#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import argparse
import time
import subprocess
import os
import locale
from sqlalchemy import create_engine, text, dialects
from sqlalchemy.exc import OperationalError
from .EventWriter import event_writer as ewr
from .semantics.mpi_event_encoding import *


def main():
    locale.setlocale(locale.LC_ALL, '')

    class ShowVersion(argparse.Action):
        def __call__(self, parser, namespace, values, option_string):
            print("nsys2prv v0.2.1")
            parser.exit() # exits the program with no more arg parsing and checking


    parser = argparse.ArgumentParser(description="Translate a NVIDIA Nsight System trace to a Paraver trace",
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                    epilog="The nsys executable needs to be in the PATH, or the environment variable NSYS_HOME needs to be set.  If using postprocessing, the PARAVER_HOME variable needs to be set.")

    parser.add_argument("-v", "--version",  nargs=0, help="Show version and exit.", action=ShowVersion)
    parser.add_argument("-f", "--filter-nvtx", help="Filter by this NVTX range")
    parser.add_argument("-t", "--trace", help="Comma separated names of events to translate: [mpi_event_trace, nvtx_pushpop_trace, nvtx_startend_trace, cuda_api_trace, gpu_metrics, openacc]")

    parser.add_argument("--force-sqlite", action="store_true", help="Force Nsight System to export SQLite database")

    parser.add_argument("-s", "--sort", action="store_true", help="Sort trace at the end")
    parser.add_argument("-z", "--compress", action="store_true", help="Compress trace at the end with gzip")

    #parser.add_argument("-n", "--nvtx-stack-range", nargs=2, type=int)

    parser.add_argument("source_rep", help="Nsight source report file")
    parser.add_argument("output", help="Paraver output trace name")

    args = parser.parse_args()

    # # Trace configuration and setup

    use_path = True

    if 'NSYS_HOME' in os.environ:
        NSYS_HOME = os.path.abspath(os.getenv('NSYS_HOME'))
        use_path = False
    
    PARAVER_HOME = os.getenv('PARAVER_HOME')

    REPORT_FILE = os.path.abspath(args.source_rep)
    REPORT_DIR = os.path.dirname(REPORT_FILE)
    trace_name = args.output

    NVTX_FILTER = args.filter_nvtx != None
    NVTX_RANGE = args.filter_nvtx

    reports = args.trace.split(",")
    reports.append('cuda_gpu_trace') # Manually add the mandatory kernel info

    reports_og = reports.copy()

    t_nvtx = False
    t_nvtx_startend = False
    t_apicalls = False
    t_mpi = False
    t_metrics = False
    t_openacc = False

    if "nvtx_pushpop_trace" in reports: t_nvtx = True 
    if "cuda_api_trace" in reports: t_apicalls = True
    if "mpi_event_trace" in reports: 
        t_mpi = True
        reports.remove("mpi_event_trace")
    if "gpu_metrics" in reports: 
        t_metrics = True
        reports.remove("gpu_metrics")
    if "nvtx_startend_trace" in reports: 
        t_nvtx_startend = True
        reports.remove("nvtx_startend_trace")
    if "openacc" in reports:
        t_openacc = True
        reports.remove("openacc")

    event_type_kernels = 63000006
    event_type_memcopy_size = 63000002
    event_type_api = 63000000
    event_type_nvtx = 9003
    event_type_nvtx_startend = 9004
    event_types_block_grid_values = [9101, 9102, 9103, 9104, 9105, 9106]
    event_types_block_grid_values_names = ['GrdX', 'GrdY', 'GrdZ', 'BlkX', 'BlkY', 'BlkZ']
    event_type_registers_thread = 9107
    event_type_correlation = 9200
    event_type_mpi = 9300
    event_type_metrics_base = 9400

    event_type_openacc = 66000000
    event_type_openacc_data = 66000001
    event_type_openacc_launch = 66000002

    event_type_name_openacc = 66100000
    event_type_name_openacc_data = 66100001
    event_type_name_openacc_launch = 66100002

    event_type_func_openacc = 66200000
    event_type_func_openacc_data = 66200001
    event_type_func_openacc_launch = 66200002

    event_type_openacc_data_size = 66300001

    comm_tag_launch = 55001
    comm_tag_memory = 55002
    comm_tag_dependency = 55003

    nvtx_select_frames = False
    nvtx_stack_top = 1
    nvtx_stack_bottom = 4


    def build_nsys_stats_name(report_name):
        base_name = os.path.splitext(os.path.basename(REPORT_FILE))[0]
        if NVTX_FILTER:
            return os.path.join(REPORT_DIR, base_name+"_{}_nvtx={}.csv".format(report_name, NVTX_RANGE))
        else:
            return os.path.join(REPORT_DIR, base_name+"_{}.csv".format(report_name))


    print("Extracting reports for: {}".format(reports_og))
    if use_path:
        nsys_call = ("nsys",)
    else:
        nsys_call = (os.path.join(NSYS_HOME, "bin/nsys"),)
    
    nsys_call += ("stats", "-r", ",".join(reports), 
                "--timeunit", "nsec", "-f", "csv", 
                "--force-overwrite", "true", "-o", ".")

    if NVTX_FILTER:
        nsys_call += ("--filter-nvtx="+NVTX_RANGE,)

    if args.force_sqlite:
        nsys_call += ("--force-export", "true")

    nsys_call += (REPORT_FILE,)

    try:
        with subprocess.Popen(nsys_call, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as p:
            for line in p.stdout:
                print(line.decode(), end='')

        if p.returncode != 0:
            raise ChildProcessError(p.returncode, p.args)
    except FileNotFoundError:
        print("You don't have an Nsight Systems installation in your PATH. Please install, Nsight Systems, or locate your installation using PATH or setting NSYS_HOME environment variable.")
        exit(1)



    print("Importing datasets...")

    kernels_df = pd.read_csv(build_nsys_stats_name("cuda_gpu_trace"))
    kernels_df.rename(columns={"CorrId": "CorrID"}, inplace=True)

    engine = create_engine(f"sqlite:///{os.path.splitext(REPORT_FILE)[0]}.sqlite")

    if t_apicalls:
        cuda_api_df = pd.read_csv(build_nsys_stats_name("cuda_api_trace"))
    else:
        cuda_api_df = pd.DataFrame()

    if t_nvtx:
        nvtx_df = pd.read_csv(build_nsys_stats_name("nvtx_pushpop_trace"))
    else:
        nvtx_df = pd.DataFrame()

    if t_nvtx_startend:
        with engine.connect() as conn, conn.begin():
            with open(os.path.join(os.path.dirname(__file__), 'scripts/nvtx_startend_trace.sql'), 'r') as query:
                nvtx_startend_df = pd.read_sql_query(text(query.read()), conn)
    else:
        nvtx_startend_df = pd.DataFrame()

    if t_mpi:
        with engine.connect() as conn, conn.begin():
            try:
                with open(os.path.join(os.path.dirname(__file__), 'scripts/mpi_p2p.sql'), 'r') as query:
                    if conn.dialect.has_table(connection=conn, table_name='MPI_P2P_EVENTS') and conn.dialect.has_table(connection=conn, table_name='MPI_START_WAIT_EVENTS'):
                        mpi_p2p_df = pd.read_sql_query(text(query.read()), conn)
                        mpi_p2p_df["event_type"] = MPITYPE_PTOP
                    else: mpi_p2p_df = pd.DataFrame()
                with open(os.path.join(os.path.dirname(__file__), 'scripts/mpi_coll.sql'), 'r') as query:
                    if conn.dialect.has_table(connection=conn, table_name='MPI_COLLECTIVES_EVENTS'):
                        mpi_coll_df = pd.read_sql_query(text(query.read()), conn)
                        mpi_coll_df = mpi_coll_df.drop(mpi_coll_df[mpi_coll_df["Event"].str.contains("File") ].index)
                        mpi_coll_df["event_type"] = MPITYPE_COLLECTIVE
                    else: mpi_coll_df = pd.DataFrame()
                with open(os.path.join(os.path.dirname(__file__), 'scripts/mpi_other.sql'), 'r') as query:
                    if conn.dialect.has_table(connection=conn, table_name='MPI_OTHER_EVENTS'):
                        mpi_other_df = pd.read_sql_query(text(query.read()), conn)
                        mpi_other_df = mpi_other_df.drop(mpi_other_df[mpi_other_df["Event"].str.contains("File") ].index)
                        mpi_other_df = mpi_other_df.drop(mpi_other_df[mpi_other_df["Event"].str.contains("Win|MPI_Get|MPI_Put|Accumulate") ].index)
                        mpi_other_df["event_type"] = MPITYPE_OTHER
                    else: mpi_other_df = pd.DataFrame()
                with open(os.path.join(os.path.dirname(__file__), 'scripts/mpi_other.sql'), 'r') as query:
                    if conn.dialect.has_table(connection=conn, table_name='MPI_OTHER_EVENTS'):
                        mpi_rma_df = pd.read_sql_query(text(query.read()), conn)
                        mpi_rma_df = mpi_rma_df[mpi_rma_df["Event"].str.contains("Win|MPI_Get|MPI_Put|Accumulate")]
                        mpi_rma_df["event_type"] = MPITYPE_RMA
                    else: mpi_rma_df = pd.DataFrame()
                with open(os.path.join(os.path.dirname(__file__), 'scripts/mpi_io.sql'), 'r') as query:
                    if conn.dialect.has_table(connection=conn, table_name='MPI_OTHER_EVENTS') and conn.dialect.has_table(connection=conn, table_name='MPI_COLLECTIVES_EVENTS'):
                        mpi_io_df = pd.read_sql_query(text(query.read()), conn)
                        mpi_io_df = mpi_io_df[mpi_io_df["Event"].str.contains("File")]
                        mpi_io_df["event_type"] = MPITYPE_IO
                    else: mpi_io_df = pd.DataFrame()
                mpi_df = pd.concat([mpi_p2p_df, mpi_coll_df, mpi_other_df, mpi_rma_df, mpi_io_df])
            except OperationalError as oe:
                print("There has been a problem fetching MPI information. MPI data will be skipped.")
                print(f"[ERROR]: {oe.detail}")
                t_mpi = False
        #mpi_df = pd.read_csv(build_nsys_stats_name("mpi_event_trace"))
    else:
        #mpi_df = pd.DataFrame()
        mpi_p2p_df = pd.DataFrame()
        mpi_coll_df = pd.DataFrame()
        mpi_other_df = pd.DataFrame()
        mpi_rma_df = pd.DataFrame()
        mpi_io_df = pd.DataFrame()

    # Obtain context Info
    context_info = pd.read_sql_table("TARGET_INFO_CUDA_CONTEXT_INFO", f"sqlite:///{os.path.splitext(REPORT_FILE)[0]}.sqlite")
    if t_mpi:
        mpi_query = "SELECT globalTid / 0x1000000 % 0x1000000 AS Pid, globalTid % 0x1000000 AS Tid, rank FROM MPI_RANKS;"
        with engine.connect() as conn, conn.begin():
            rank_info = pd.read_sql_query(mpi_query, conn)
    
    context_info.sort_values(["processId"], inplace=True)

    if t_metrics:
        gpu_metrics = pd.read_sql_table("GPU_METRICS", f"sqlite:///{os.path.splitext(REPORT_FILE)[0]}.sqlite")
        metrics_description = pd.read_sql_table("TARGET_INFO_GPU_METRICS", f"sqlite:///{os.path.splitext(REPORT_FILE)[0]}.sqlite")
        gpu_metrics.drop(gpu_metrics[gpu_metrics["rawTimestamp"] < 0].index, inplace=True) # drop negative time
        metrics_event_names = metrics_description.groupby(["metricId"]).agg({'metricName': 'first'}).reset_index()
        metrics_event_names["metricId"] = metrics_event_names["metricId"] + event_type_metrics_base
        #gpu_metrics["task"] = gpu_metrics.groupby(["typeId"]).ngroup() + 1
        gpu_metrics["deviceId"] = gpu_metrics["typeId"].apply(lambda x: x & 0xFF)
        gpu_metrics_agg = gpu_metrics.groupby(["timestamp", "typeId"]).agg({'metricId': lambda x: list(x+event_type_metrics_base),
                                                                        'value': lambda x: list(x),
                                                                        'deviceId': 'first'})
        gpu_metrics_agg.reset_index(inplace=True)


    if t_openacc:
        with engine.connect() as conn, conn.begin():
            with open(os.path.join(os.path.dirname(__file__), 'scripts/openacc_other.sql'), 'r') as query:
                openacc_other_df = pd.read_sql_query(text(query.read()), conn)
            with open(os.path.join(os.path.dirname(__file__), 'scripts/openacc_launch.sql'), 'r') as query:
                openacc_launch_df = pd.read_sql_query(text(query.read()), conn)
            with open(os.path.join(os.path.dirname(__file__), 'scripts/openacc_data.sql'), 'r') as query:
                openacc_data_df = pd.read_sql_query(text(query.read()), conn)
            openacc_event_kind = pd.read_sql_table("ENUM_OPENACC_EVENT_KIND", conn)


    # # Building object model

    # ## Tasks and threads
    # Now, find unique appearences of ThreadID and ProcessID

    if t_apicalls: print("CUDA calls unique processes: {}, and unique threads: {}".format(cuda_api_df["Pid"].unique(), cuda_api_df["Tid"].unique()))
    if t_nvtx: print("NVTX ranges unique processes: {}, and unique threads: {}".format(nvtx_df["PID"].unique(), nvtx_df["TID"].unique()))
    if t_nvtx_startend: print("NVTX startend unique processes: {}, and unique threads: {}".format(nvtx_startend_df["Pid"].unique(), nvtx_startend_df["Tid"].unique()))
    if t_mpi: print("MPI calls unique processes: {}, and unique threads: {}".format(mpi_df["Pid"].unique(), mpi_df["Tid"].unique()))
    if t_openacc: print("OpenACC calls unique processes: {}, and unique threads: {}".format(openacc_other_df["Pid"].unique(), openacc_other_df["Tid"].unique()))

    if t_nvtx: nvtx_df.rename(columns={"PID":"Pid", "TID":"Tid"}, inplace=True)

    compute_threads_with = []
    if t_apicalls: compute_threads_with.append(cuda_api_df[['Pid', 'Tid']])
    if t_nvtx: compute_threads_with.append(nvtx_df[["Pid", "Tid"]])
    if t_nvtx_startend: compute_threads_with.append(nvtx_startend_df[["Pid", "Tid"]])
    if t_mpi: compute_threads_with.append(mpi_df[["Pid", "Tid"]])
    if t_openacc: compute_threads_with.append(openacc_other_df[["Pid", "Tid"]])


    threads = pd.concat(compute_threads_with).drop_duplicates()
    if t_mpi:
        threads["Rank"] = threads["Pid"].map(rank_info.set_index("Pid")["rank"])
        threads.sort_values(["Rank"], inplace=True)
    else:
        threads.sort_values(["Pid"], inplace=True)
    threads["thread"] = threads.groupby(["Pid"]).cumcount() + 1
    threads["task"] = threads.groupby(["Pid"]).ngroup() + 1
    threads["device"] = threads["Pid"].map(context_info[context_info["contextId"] == 1].set_index("processId")["deviceId"])
    #threads.sort_values(["task", "thread"], inplace=True)
    threads.reset_index()

    tasks_set = threads.groupby(["task"]).agg({'Pid': 'first',
                                        'Tid': lambda x: set(x),
                                            'thread': 'count',
                                            'device': 'first' })

    cuda_api_df["thread"] = 0
    cuda_api_df["task"] = 0
    nvtx_df["thread"] = 0
    nvtx_df["task"] = 0
    nvtx_startend_df["thread"] = 0
    nvtx_startend_df["task"] = 0

    if t_openacc:
        openacc_other_df["thread"] = 0
        openacc_other_df["task"] = 0
        openacc_launch_df["thread"] = 0
        openacc_launch_df["task"] = 0
        openacc_data_df["thread"] = 0
        openacc_data_df["task"] = 0

    threads['row_name'] = "THREAD 1." + threads['task'].astype(str) + '.' + threads['thread'].astype(str)

    # for index,row in cuda_api_df.iterrows():
    #     cuda_api_df.at[index, "thread"] = threads.at[(threads["Tid"] == row["Tid"]).idxmax(), "thread"]
    #     cuda_api_df.at[index, "task"] = threads.at[(threads["Tid"] == row["Tid"]).idxmax(), "task"]

    # for index,row in nvtx_df.iterrows():
    #     nvtx_df.at[index, "thread"] = threads.at[(threads["Tid"] == row["Tid"]).idxmax(), "thread"]
    #     nvtx_df.at[index, "task"] = threads.at[(threads["Tid"] == row["Tid"]).idxmax(), "task"]

    if t_apicalls:
        cuda_api_df["thread"] = cuda_api_df["Tid"].map(threads.set_index('Tid')["thread"])
        cuda_api_df["task"] = cuda_api_df["Tid"].map(threads.set_index('Tid')["task"])

    if t_nvtx:
        nvtx_df["thread"] = nvtx_df["Tid"].map(threads.set_index('Tid')["thread"])
        nvtx_df["task"] = nvtx_df["Tid"].map(threads.set_index('Tid')["task"])

    if t_nvtx_startend:
        nvtx_startend_df["thread"] = nvtx_startend_df["Tid"].map(threads.set_index('Tid')["thread"])
        nvtx_startend_df["task"] = nvtx_startend_df["Tid"].map(threads.set_index('Tid')["task"])

    if t_mpi:
        mpi_df["thread"] = mpi_df["Tid"].map(threads.set_index('Tid')["thread"])
        mpi_df["task"] = mpi_df["Tid"].map(threads.set_index('Tid')["task"])

    if t_openacc:
        openacc_other_df["thread"] = openacc_other_df["Tid"].map(threads.set_index('Tid')["thread"])
        openacc_other_df["task"] = openacc_other_df["Tid"].map(threads.set_index('Tid')["task"])
        openacc_launch_df["thread"] = openacc_launch_df["Tid"].map(threads.set_index('Tid')["thread"])
        openacc_launch_df["task"] = openacc_launch_df["Tid"].map(threads.set_index('Tid')["task"])
        openacc_data_df["thread"] = openacc_data_df["Tid"].map(threads.set_index('Tid')["thread"])
        openacc_data_df["task"] = openacc_data_df["Tid"].map(threads.set_index('Tid')["task"])


    # 
    # ## GPU devices
    # First, detect number of devices and streams.  To respect Paraver's resource model, we will create a THREAD for each stream. To do that, select each unique pair of Device and Stream and assign an incremental ID.


    streams = kernels_df[['Device', 'Strm']].drop_duplicates()
    streams["thread"] = streams.groupby(["Device"]).cumcount() + 1
    streams["deviceid"] = streams.sort_values("Device").groupby(["Device"]).ngroup()
    streams["Pid"] = streams["deviceid"].map(tasks_set.set_index("device")["Pid"])
    streams["task"] = streams["deviceid"].map(tasks_set.reset_index().set_index("device")["task"])

    streams['row_name'] = 'CUDA-D'+streams['deviceid'].astype(str) + '.S' + streams['Strm'].astype(str)
    num_streams = streams.count().iloc[0]
    streams.sort_values(["Pid", "thread"], inplace=True)
    streams.reset_index(inplace=True)

    devices_set = streams.groupby(["deviceid"]).agg({'Device': 'first',
                                        'Strm': lambda x: set(x),
                                            'thread': 'count',
                                            'task': 'first',
                                            'Pid': 'last'})

    # Here we finally update the threadId we are going to put in the event record of kernel executions to respect the normal threads before CUDA streams

    num_normal_threads = tasks_set['thread']
    num_normal_threads_repeated = num_normal_threads.repeat(devices_set["thread"]).reset_index()[["thread"]]


    streams['thread'] = streams['thread'] + num_normal_threads_repeated["thread"]
    # for index,row in kernels_df.iterrows():
    #     kernels_df.at[index, "thread"] = streams.at[(streams["Strm"] == row["Strm"]).idxmax(), "thread"]
    #     kernels_df.at[index, "deviceid"] = streams.at[(streams["Device"] == row["Device"]).idxmax(), "deviceid"]

    # More efficient way by chatgpt
    # First, let's filter streams DataFrame based on conditions
    filtered_streams = streams.groupby(["Device", "Strm"]).agg({'thread':'first', 'task':'first'}).reset_index()
    # Now, merge the filtered streams DataFrame with kernels_df
    result_df = kernels_df.merge(filtered_streams, how='left', on=['Device', 'Strm'])
    # Copy the results back to kernels_df
    kernels_df['thread'] = result_df['thread']
    kernels_df['task'] = result_df['task']

    # Add auxiliary stream to streams dataframe
    if t_metrics:
        aux_streams = devices_set.reset_index()[["deviceid", "Device", "thread", "task"]]
        aux_streams["Strm"] = 99
        aux_streams["row_name"] = "Metrics GPU"+aux_streams["deviceid"].astype(str)
        aux_streams["Pid"] = aux_streams["deviceid"].map(tasks_set.set_index('device')["Pid"])
        aux_streams["thread"] = aux_streams["thread"] + aux_streams["deviceid"].map(tasks_set.set_index('device')['thread']) + 1
        gpu_metrics_agg["task"] = gpu_metrics_agg["deviceId"].map(devices_set["task"])
        gpu_metrics_agg["thread"] = gpu_metrics_agg["task"].map(aux_streams.set_index('task')["thread"])
        streams = pd.concat([streams, aux_streams]).sort_values(['task', 'thread'])



    # ## Writing ROW file
    # Now we can write the _row_ file with this information

    print(tasks_set)
    print(devices_set)

    print("  -Writing resource model to row file...")

    row_df = pd.concat([threads[["thread", "task", "row_name"]], streams[["thread", "task", "row_name"]]])
    row_df.sort_values(["task", "thread"], inplace=True)

    with open(trace_name+".row", "w") as row_file:
        # MISSING NODE INFORMATION, EITHER GET FROM TRACE OR ASK USER
        row_file.write("LEVEL NODE SIZE 1\nnode1\n\n")

        row_file.write("LEVEL THREAD SIZE {}\n".format(len(row_df.index)))
        for index, row in row_df.iterrows():
            row_file.write("{}\n".format(row["row_name"]))

        row_file.write("\n")


    # # Collecting event values
    # Second step is collect all different event values for CUDA API calls, kernel names, and NVTX ranges.  Each of these define a different event type, and will need unique identifiers to be used as a event values.  Finally these needs to be dumped to the PCF file.

    print("Collecting event names and information...")

    if t_apicalls:
        cuda_api_df["event_value"] = cuda_api_df.groupby(["Name"]).ngroup() + 1
        api_call_names = cuda_api_df[['Name', 'event_value']].drop_duplicates()
        api_call_names.sort_values("event_value", inplace=True)

    # if t_mpi:
    #     mpi_df["event_value"] = mpi_df.groupby(["Event"]).ngroup() + 1
    #     mpi_names = mpi_df[['Event', 'event_value']].drop_duplicates()
    #     mpi_names.sort_values("event_value", inplace=True)
    
    if t_mpi:
        mpi_values = pd.DataFrame.from_dict(MPIVal, orient='index', columns=["event_value"])
        mpi_names = pd.DataFrame.from_dict(MPI_Val_Labels, orient='index', columns=["Name"])
        mpi_names = mpi_names.merge(mpi_values, left_index=True, right_index=True)
        mpi_df["event_value"] = mpi_df["Event"].map(mpi_names.set_index('Name')["event_value"])



    kernels_df["event_value"] = kernels_df.groupby(["Name"]).ngroup() + 1 + api_call_names.count().iloc[0] # Add padding to event values so CUDA calls and CUDA kernels can be added
    kernel_names = kernels_df[['event_value', 'Name']].drop_duplicates()
    kernel_names.sort_values("event_value", inplace=True)
    # Remove brackets from names
    kernel_names["Name"] = kernel_names["Name"].apply(lambda x: x.replace("[", "").replace("]", ""))

    if t_nvtx:
        nvtx_df_subset = nvtx_df
        lower_level = max(nvtx_df["Lvl"])

        if nvtx_select_frames:
            #subset of df
            nvtx_df_subset = nvtx_df[(nvtx_df["Lvl"] >= nvtx_stack_top) & (nvtx_df["Lvl"] <= nvtx_stack_bottom)]

        nvtx_df_subset["event_value"] = nvtx_df_subset.groupby(["Name"]).ngroup() + 1
        #nvtx_df_subset["event_value"] = nvtx_df_subset["RangeId"]
        ranges_names = nvtx_df_subset[['event_value', 'Name']].drop_duplicates()
        ranges_names.sort_values("event_value", inplace=True)

    if t_nvtx_startend:
        nvtx_startend_df["event_value"] = nvtx_startend_df.groupby(["tag"]).ngroup() + 1
        nvtx_startend_names = nvtx_startend_df[['tag', 'event_value']].drop_duplicates()
        nvtx_startend_names.sort_values("event_value", inplace=True)
        nvtx_startend_names

    if t_openacc:
        openacc_event_kind["id"] += 1
        openacc_launch_df["eventKind"] += 1
        openacc_data_df["eventKind"] += 1
        openacc_other_df["eventKind"] += 1

        openacc_data_df["name_value"] = openacc_data_df.groupby(["name"], dropna=False).ngroup() + 1
        openacc_full_data_names = openacc_data_df[['name_value', 'name']].drop_duplicates()
        openacc_full_data_names.sort_values(["name_value"], inplace=True)

        openacc_launch_df["name_value"] = openacc_launch_df.groupby(["name"], dropna=False).ngroup() + 1 + openacc_full_data_names.count().iloc[0]
        openacc_full_launch_names = openacc_launch_df[['name_value', 'name']].drop_duplicates()
        openacc_full_launch_names.sort_values(["name_value"], inplace=True)

        openacc_other_df["name_value"] = openacc_other_df.groupby(["name"], dropna=False).ngroup() + 1 + openacc_full_data_names.count().iloc[0] + openacc_full_launch_names.count().iloc[0]
        openacc_full_other_names = openacc_other_df[['name_value', 'name']].drop_duplicates()
        openacc_full_other_names.sort_values(["name_value"], inplace=True)

        openacc_data_df["func_value"] = openacc_data_df.groupby(["func"], dropna=False).ngroup() + 1
        openacc_full_data_funcs = openacc_data_df[['func_value', 'func']].drop_duplicates()
        openacc_full_data_funcs.sort_values(["func_value"], inplace=True)

        openacc_launch_df["func_value"] = openacc_launch_df.groupby(["func"], dropna=False).ngroup() + 1 + openacc_full_data_funcs.count().iloc[0]
        openacc_full_launch_funcs = openacc_launch_df[['func_value', 'func']].drop_duplicates()
        openacc_full_launch_funcs.sort_values(["func_value"], inplace=True)

        openacc_other_df["func_value"] = openacc_other_df.groupby(["func"], dropna=False).ngroup() + 1 + openacc_full_data_funcs.count().iloc[0] + openacc_full_launch_funcs.count().iloc[0]
        openacc_full_other_funcs = openacc_other_df[['func_value', 'func']].drop_duplicates()
        openacc_full_other_funcs.sort_values(["func_value"], inplace=True)



    print("-\tWriting pcf file...")

    with open(trace_name+".pcf", "w") as pcf_file:

        CONFIG = """
        DEFAULT_OPTIONS

        LEVEL               THREAD
        UNITS               NANOSEC
        LOOK_BACK           100
        SPEED               1
        FLAG_ICONS          ENABLED
        NUM_OF_STATE_COLORS 1000
        YMAX_SCALE          37


        DEFAULT_SEMANTIC

        THREAD_FUNC          State As Is

        GRADIENT_COLOR
        0    {0,255,2}
        1    {0,244,13}
        2    {0,232,25}
        3    {0,220,37}
        4    {0,209,48}
        5    {0,197,60}
        6    {0,185,72}
        7    {0,173,84}
        8    {0,162,95}
        9    {0,150,107}
        10    {0,138,119}
        11    {0,127,130}
        12    {0,115,142}
        13    {0,103,154}
        14    {0,91,166}


        GRADIENT_NAMES
        0    Gradient 0
        1    Grad. 1/MPI Events
        2    Grad. 2/OMP Events
        3    Grad. 3/OMP locks
        4    Grad. 4/User func
        5    Grad. 5/User Events
        6    Grad. 6/General Events
        7    Grad. 7/Hardware Counters
        8    Gradient 8
        9    Gradient 9
        10    Gradient 10
        11    Gradient 11
        12    Gradient 12
        13    Gradient 13
        14    Gradient 14

        """

        pcf_file.write(CONFIG)

        if t_apicalls:
            pcf_file.write("EVENT_TYPE\n")
            pcf_file.write("0 {} CUDA library call\n".format(event_type_api))
            pcf_file.write("VALUES\n")
            pcf_file.write("0 End\n")
            for index, row in api_call_names.iterrows():
                pcf_file.write("{} {}\n".format(row["event_value"], row["Name"]))
            pcf_file.write("\n")

        if t_mpi:
            pcf_file.write("EVENT_TYPE\n")
            pcf_file.write("0 {} {}\n".format(MPITYPE_PTOP, MPI_Type_Labels["MPITYPE_PTOP"]))
            pcf_file.write("VALUES\n")
            pcf_file.write("0 End\n")
            for index, row in mpi_names.iterrows():
                pcf_file.write("{} {}\n".format(row["event_value"], row["Name"]))
            pcf_file.write("\n")
            pcf_file.write("EVENT_TYPE\n")
            pcf_file.write("0 {} {}\n".format(MPITYPE_COLLECTIVE, MPI_Type_Labels["MPITYPE_COLLECTIVE"]))
            pcf_file.write("VALUES\n")
            pcf_file.write("0 End\n")
            for index, row in mpi_names.iterrows():
                pcf_file.write("{} {}\n".format(row["event_value"], row["Name"]))
            pcf_file.write("\n")
            pcf_file.write("EVENT_TYPE\n")
            pcf_file.write("0 {} {}\n".format(MPITYPE_OTHER, MPI_Type_Labels["MPITYPE_OTHER"]))
            pcf_file.write("VALUES\n")
            pcf_file.write("0 End\n")
            for index, row in mpi_names.iterrows():
                pcf_file.write("{} {}\n".format(row["event_value"], row["Name"]))
            pcf_file.write("\n")
            pcf_file.write("EVENT_TYPE\n")
            pcf_file.write("0 {} {}\n".format(MPITYPE_RMA, MPI_Type_Labels["MPITYPE_RMA"]))
            pcf_file.write("VALUES\n")
            pcf_file.write("0 End\n")
            for index, row in mpi_names.iterrows():
                pcf_file.write("{} {}\n".format(row["event_value"], row["Name"]))
            pcf_file.write("\n")
            pcf_file.write("EVENT_TYPE\n")
            pcf_file.write("0 {} {}\n".format(MPITYPE_IO, MPI_Type_Labels["MPITYPE_IO"]))
            pcf_file.write("VALUES\n")
            pcf_file.write("0 End\n")
            for index, row in mpi_names.iterrows():
                pcf_file.write("{} {}\n".format(row["event_value"], row["Name"]))
            pcf_file.write("\n")
            pcf_file.write("EVENT_TYPE\n")
            pcf_file.write("1 {} {}\n".format(MPITYPE_SEND_GLOBAL_SIZE, "Send Size in MPI Global OP"))
            pcf_file.write("1 {} {}\n".format(MPITYPE_RECV_GLOBAL_SIZE, "Recv Size in MPI Global OP"))
            pcf_file.write("\n")

        pcf_file.write("EVENT_TYPE\n")
        pcf_file.write("0 {} CUDA kernel\n".format(event_type_kernels))
        pcf_file.write("VALUES\n")
        pcf_file.write("0 End\n")
        for index, row in kernel_names.iterrows():
            pcf_file.write("{} {}\n".format(row["event_value"], row["Name"]))
        pcf_file.write("\n")

        pcf_file.write("EVENT_TYPE\n")
        for i, v in enumerate(event_types_block_grid_values_names):
            pcf_file.write("0 {} Kernel {}\n".format(event_types_block_grid_values[i], v))
        pcf_file.write("0 {} Kernel Registers/Thread\n".format(event_type_registers_thread))
        pcf_file.write("0 {} Memcopy size\n".format(event_type_memcopy_size))
        pcf_file.write("0 {} Correlation ID\n".format(event_type_correlation))
        pcf_file.write("\n")

        if t_metrics:
            pcf_file.write("EVENT_TYPE\n")
            for i, r in metrics_event_names.iterrows():
                pcf_file.write("7 {} {}\n".format(r["metricId"], r["metricName"]))
            pcf_file.write("\n")

        if t_nvtx:
            pcf_file.write("EVENT_TYPE\n")
            pcf_file.write("0 {} NVTX pushpop ranges\n".format(event_type_nvtx))
            pcf_file.write("VALUES\n")
            pcf_file.write("0 End\n")
            for index, row in ranges_names.iterrows():
                pcf_file.write("{} {}\n".format(row["event_value"], row["Name"]))
            pcf_file.write("\n")

        if t_nvtx_startend:
            pcf_file.write("EVENT_TYPE\n")
            pcf_file.write("0 {} NVTX startend ranges\n".format(event_type_nvtx_startend))
            pcf_file.write("VALUES\n")
            pcf_file.write("0 End\n")
            for index, row in nvtx_startend_names.iterrows():
                pcf_file.write("{} {}\n".format(row["event_value"], row["tag"]))

        if t_openacc:
            pcf_file.write("EVENT_TYPE\n")
            pcf_file.write("0 {} OpenACC Data Events\n".format(event_type_openacc_data))
            pcf_file.write("VALUES\n")
            pcf_file.write("0 End\n")
            for index, row in openacc_event_kind.iterrows():
                pcf_file.write("{} {}\n".format(row["id"], row["label"]))
            pcf_file.write("\n")

            pcf_file.write("EVENT_TYPE\n")
            pcf_file.write("0 {} OpenACC Launch Events\n".format(event_type_openacc_launch))
            pcf_file.write("VALUES\n")
            pcf_file.write("0 End\n")
            for index, row in openacc_event_kind.iterrows():
                pcf_file.write("{} {}\n".format(row["id"], row["label"]))
            pcf_file.write("\n")

            pcf_file.write("EVENT_TYPE\n")
            pcf_file.write("0 {} OpenACC Other Events\n".format(event_type_openacc))
            pcf_file.write("VALUES\n")
            pcf_file.write("0 End\n")
            for index, row in openacc_event_kind.iterrows():
                pcf_file.write("{} {}\n".format(row["id"], row["label"]))
            pcf_file.write("\n")

            pcf_file.write("EVENT_TYPE\n")
            pcf_file.write("0 {} OpenACC data region source\n".format(event_type_name_openacc_data))
            pcf_file.write("VALUES\n")
            pcf_file.write("0 End\n")
            for index, row in openacc_full_data_names.iterrows():
                pcf_file.write("{} {}\n".format(row["name_value"], row["name"]))
            pcf_file.write("\n")

            pcf_file.write("EVENT_TYPE\n")
            pcf_file.write("0 {} OpenACC launch region source\n".format(event_type_name_openacc_launch))
            pcf_file.write("VALUES\n")
            pcf_file.write("0 End\n")
            for index, row in openacc_full_launch_names.iterrows():
                pcf_file.write("{} {}\n".format(row["name_value"], row["name"]))
            pcf_file.write("\n")

            pcf_file.write("EVENT_TYPE\n")
            pcf_file.write("0 {} OpenACC other region source\n".format(event_type_name_openacc))
            pcf_file.write("VALUES\n")
            pcf_file.write("0 End\n")
            for index, row in openacc_full_other_names.iterrows():
                pcf_file.write("{} {}\n".format(row["name_value"], row["name"]))
            pcf_file.write("\n")

            pcf_file.write("EVENT_TYPE\n")
            pcf_file.write("0 {} OpenACC data function name\n".format(event_type_func_openacc_data))
            pcf_file.write("VALUES\n")
            pcf_file.write("0 End\n")
            for index, row in openacc_full_data_funcs.iterrows():
                pcf_file.write("{} {}\n".format(row["func_value"], row["func"]))
            pcf_file.write("\n")

            pcf_file.write("EVENT_TYPE\n")
            pcf_file.write("0 {} OpenACC launch function name\n".format(event_type_func_openacc_launch))
            pcf_file.write("VALUES\n")
            pcf_file.write("0 End\n")
            for index, row in openacc_full_launch_funcs.iterrows():
                pcf_file.write("{} {}\n".format(row["func_value"], row["func"]))
            pcf_file.write("\n")

            pcf_file.write("EVENT_TYPE\n")
            pcf_file.write("0 {} OpenACC other function name\n".format(event_type_func_openacc))
            pcf_file.write("VALUES\n")
            pcf_file.write("0 End\n")
            for index, row in openacc_full_other_funcs.iterrows():
                pcf_file.write("{} {}\n".format(row["func_value"], row["func"]))
            pcf_file.write("\n")

    # # Split of kernel execution between compute and memory


    memops_names = ["[CUDA memcpy Device-to-Device]", "[CUDA memcpy Device-to-Host]", "[CUDA memcpy Host-to-Device]", "[CUDA memset]", "[CUDA memcpy Peer-to-Peer]"]
    memops_df = kernels_df.loc[kernels_df["Name"].isin(memops_names)]
    mask = ~kernels_df.index.isin(memops_df.index)
    kernels_df = kernels_df.loc[mask] #Only keep non-memory kernels
    memops_df["bytes_b"] = memops_df["Bytes (MB)"].astype("str", copy=True).apply(lambda x: int(locale.atof(x)*1000000)).astype("int")

    # # Communications
    comm_kernel_df = cuda_api_df.merge(kernels_df, how="inner", left_on=["CorrID", "task"], right_on=["CorrID", "task"], suffixes=("_call", "_k"), validate="many_to_one")
    comm_memory_df = cuda_api_df.merge(memops_df, how="inner", left_on=["CorrID", "task"], right_on=["CorrID", "task"], suffixes=("_call", "_mem"), validate="one_to_one")


    # # Timeline reconstruction

    print("Reconstructing timeline...")

    def create_event_record(start, dur, thread, task, type, value):
        begin = "2:0:1:{}:{}:{}:{}:{}\n".format(task, thread, start, type, value)
        end   = "2:0:1:{}:{}:{}:{}:{}\n".format(task, thread, start+dur, type, 0)
        return begin+end

    def create_combined_events_record(start, dur, thread, task, types, values):
        begin = "2:0:1:{}:{}:{}".format(task, thread, start)
        end   = "2:0:1:{}:{}:{}".format(task, thread, start+dur)
        for i, v in enumerate(types):
            begin = begin + ":{}:{}".format(v, values[i])
            end = end + ":{}:{}".format(v, 0)
        begin = begin + "\n"
        end = end + "\n"
        return begin+end

    def create_communication_record(from_task, from_thread, to_task, to_thread, time_send, time_rcv, size, tag):
        obj_send = "0:1:{0}:{1}".format(
            from_task, from_thread
        )
        obj_recv = "0:1:{0}:{1}".format(
            to_task, to_thread
        )
        return "3:"+obj_send+":{time_send}:{time_send}:".format(time_send = time_send) + obj_recv + ":{time_rcv}:{time_rcv}:{size}:{tag}\n".format(time_rcv = time_rcv, size = size, tag = tag)

    def create_metrics_record(metric_row):
        base = "2:0:1:{}:{}:{}".format(metric_row["task"], metric_row["thread"], metric_row["timestamp"])
        event_values = ""
        for pair in zip(metric_row["metricId"], metric_row["value"]):
            event_values += ":{}:{}".format(pair[0], pair[1])
        base += event_values
        base += "\n"
        return base

    now = time.strftime("%d/%m/%Y at %H:%M")

    applist = "{}:(".format(len(tasks_set.index))
    for i, r in row_df.groupby(["task"]).count().iterrows():
        applist = applist + "{}:1".format(r["thread"])
        if i < len(tasks_set.index): applist = applist + ","
    applist = applist + ")"

    compute_max_with = []
    if t_apicalls: compute_max_with.append((cuda_api_df["Start (ns)"] + cuda_api_df["Duration (ns)"]).max())
    if t_nvtx: compute_max_with.append(nvtx_df["End (ns)"].max())
    if t_nvtx_startend: compute_max_with.append(nvtx_startend_df["end"].max())
    if t_mpi: compute_max_with.append(mpi_df["End:ts_ns"].max())

    ftime = max(compute_max_with)
    header = "#Paraver ({}):{}_ns:0:1:{}\n".format(now, ftime, applist)


    with open(trace_name+".prv", "w") as prv_file:
        prv_file.write(header)

        # Write events


        types = [event_type_kernels] + event_types_block_grid_values + [event_type_registers_thread, event_type_correlation]
        ewr(prv_file, kernels_df, "Kernels", lambda r:
                    (create_combined_events_record(r.iloc[0], r.iloc[1], int(r["thread"]), int(r["task"]), types, [r["event_value"]] + [int(r['GrdX']), int(r['GrdY']), int(r['GrdZ']), int(r['BlkX']), int(r['BlkY']), int(r['BlkZ']), int(r['Reg/Trd']), r["CorrID"]])))

        types_mem = [event_type_kernels, event_type_memcopy_size, event_type_correlation]
        ewr(prv_file, memops_df, "Memory operations", lambda r: 
                    (create_combined_events_record(r.iloc[0], r.iloc[1], int(r["thread"]), int(r["task"]), types_mem, [r["event_value"], r["bytes_b"], r["CorrID"]])))

        if t_apicalls:
            types_api = [event_type_api, event_type_correlation]
            ewr(prv_file, cuda_api_df, "CUDA API calls", lambda r:
                        (create_combined_events_record(r.iloc[0], r.iloc[1], int(r["thread"]), int(r["task"]), types_api, [r["event_value"], r["CorrID"]])))


        if t_nvtx:
            ewr(prv_file, nvtx_df_subset, "NVTX pushpop ranges", lambda r:
                        (create_event_record(r.iloc[0], r.iloc[2], int(r["thread"]), int(r["task"]), event_type_nvtx, r["event_value"])))

        if t_nvtx_startend:
            ewr(prv_file, nvtx_startend_df, "NVTX startend ranges", lambda r:
                        (create_event_record(r.iloc[0], r.iloc[2], int(r["thread"]), int(r["task"]), event_type_nvtx_startend, r["event_value"])))


        if t_mpi:
            def serialize_mpi(r):
                if r["Kind"] == "collectives":
                    return create_combined_events_record(r.iloc[1], r.iloc[3], int(r["thread"]), int(r["task"]), [r["event_type"], MPITYPE_SEND_GLOBAL_SIZE, MPITYPE_RECV_GLOBAL_SIZE], [r["event_value"], r["CollSendSize:mem_b"], r["CollRecvSize:mem_b"]])
                else:
                    return create_event_record(r.iloc[1], r.iloc[3], int(r["thread"]), int(r["task"]), r["event_type"], r["event_value"])
            ewr(prv_file, mpi_df, "MPI events", lambda r: serialize_mpi(r))

        if t_openacc:
            t_acc_d = [event_type_openacc_data, event_type_name_openacc_data, event_type_func_openacc_data, event_type_openacc_data_size]
            ewr(prv_file, openacc_data_df, "OpenACC data constructs", lambda r:
                        (create_combined_events_record(r["start"], r["end"] - r["start"], r["thread"], r["task"], t_acc_d, [r["eventKind"], r["name_value"], r["func_value"], r["bytes"]])))
            t_acc_l = [event_type_openacc_launch, event_type_name_openacc_launch, event_type_func_openacc_launch]
            ewr(prv_file, openacc_launch_df, "OpenACC launch constructs", lambda r:
                        (create_combined_events_record(r["start"], r["end"] - r["start"], r["thread"], r["task"], t_acc_l, [r["eventKind"], r["name_value"], r["func_value"]])))
            t_acc_o = [event_type_openacc, event_type_name_openacc, event_type_func_openacc]
            ewr(prv_file, openacc_other_df, "OpenACC other constructs", lambda r:
                        (create_combined_events_record(r["start"], r["end"] - r["start"], r["thread"], r["task"], t_acc_o, [r["eventKind"], r["name_value"], r["func_value"]])))

        if t_metrics:
            ewr(prv_file, gpu_metrics_agg, "GPU metrics", lambda r:
                        (create_metrics_record(r)))

        if t_apicalls:
            ewr(prv_file, comm_kernel_df, "Kernel correlation lines", lambda r:
                        (create_communication_record(r["task"], r["thread_call"], r["task"], r["thread_k"], (r["Start (ns)_call"]), r["Start (ns)_k"], 0, comm_tag_launch)))
            ewr(prv_file, comm_memory_df, "Memory correlation lines", lambda r:
                        (create_communication_record(r["task"], r["thread_call"], r["task"], r["thread_mem"], (r["Start (ns)_call"]), r["Start (ns)_mem"], int(r["bytes_b"]), comm_tag_memory)))


    print(f"Congratulations! Trace {trace_name}.prv correctly translated.")
    # ## Postprocessing
    # - Reorder trace
    # - GZip trace

    print("Postprocessing...")

    if args.sort:
        print("- Sorting trace...")
        args_sorter = (PARAVER_HOME+"/bin/sort-trace.awk.sh", trace_name+".prv")
        print(args_sorter)
        with subprocess.Popen(args_sorter, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as p:
            for line in p.stdout: 
                print(line.decode(), end='')

        if p.returncode != 0:
            raise ChildProcessError(p.returncode, p.args)
        
        os.remove(trace_name+".prv")
        os.remove(trace_name+".pcf")
        os.remove(trace_name+".row")

    if args.compress:
        print("- Compressing trace...")
        if args.sort:
            args_gzip = ("gzip", trace_name+".sorted.prv")
        else:
            args_gzip = ("gzip", trace_name+".prv")
        print(args_gzip)
        with subprocess.Popen(args_gzip, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as p:
            for line in p.stdout: 
                print(line.decode(), end='')

        if p.returncode != 0:
            raise ChildProcessError(p.returncode, p.args)

if __name__ == "__main__":
    main()