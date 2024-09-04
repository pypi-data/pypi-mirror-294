cimport cython
from libcpp.unordered_map cimport unordered_map
from cython.operator cimport dereference as deref, preincrement as inc
from libcpp.vector cimport vector
import threading
from libcpp.queue cimport queue
from libcpp.string cimport string
import time
import subprocess
cimport openmp
import sys
from pprint import pformat
import regex as re
from exceptdrucker import errwrite
import ctypes
re.cache_all(True)

def killthread(threadobject):
    """
    Attempts to terminate a thread by forcefully setting an asynchronous exception
    of type SystemExit in the thread's Python interpreter state. This function
    only operates on alive threads.

    Parameters:
        threadobject (threading.Thread): The thread object to terminate.

    Returns:
        bool: True if the thread was successfully found and an attempt to terminate it was made,
        False otherwise.

    Raises:
        ValueError: If threadobject does not refer to a valid active thread.
    """
    # based on https://pypi.org/project/kthread/
    if not threadobject.is_alive():
        return True
    tid = -1
    for tid1, tobj in threading._active.items():
        if tobj is threadobject:
            tid = tid1
            break
    if tid == -1:
        sys.stderr.write(f"{threadobject} not found")
        return False
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
        ctypes.c_long(tid), ctypes.py_object(SystemExit)
    )
    if res == 0:
        return False
    elif res != 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, 0)
        return False
    return True


config_settings=sys.modules[__name__]
config_settings.running_uiautomators=[]
config_settings.debug_enabled=False
config_settings.read_events_data=True
config_settings.stop=False
ctypedef queue[string] ququ
ctypedef vector[string] stringvector
ctypedef unordered_map[string,string] strmap
cdef:
    ququ my_parsing_queue
    tuple[bytes] all_categories_eventparser=(
            b"AccessibilityDataSensitive",
            b"AccessibilityFocused",
            b"AccessibilityTool",
            b"Action",
            b"Active",
            b"AddedCount",
            b"BeforeText",
            b"BooleanProperties",
            b"Checked",
            b"ClassName",
            b"ConnectionId",
            b"ContentChangeTypes",
            b"ContentDescription",
            b"ContentInvalid",
            b"CurrentItemIndex",
            b"Empty",
            b"Enabled",
            b"EventTime",
            b"EventType",
            b"Focused",
            b"FromIndex",
            b"FullScreen",
            b"ItemCount",
            b"Loggable",
            b"MaxScrollX",
            b"MaxScrollY",
            b"MovementGranularity",
            b"PackageName",
            b"ParcelableData",
            b"Password",
            b"Records",
            b"RemovedCount",
            b"ScrollDeltaX",
            b"ScrollDeltaY",
            b"ScrollX",
            b"ScrollY",
            b"Scrollable",
            b"Sealed",
            b"Source",
            b"SourceDisplayId",
            b"SourceNodeId",
            b"SourceWindowId",
            b"SpeechStateChangeTypes",
            b"Text",
            b"ToIndex",
            b"WindowChangeTypes",
            b"WindowChanges",
            b"WindowId",
            b"TimeStamp",
            b'TimeNow',
            b"recordCount",
        )

cdef class MyDict:
    cdef strmap c_dict
    cpdef int add_values(self,stringvector mykeys, stringvector myvalues) except + :
        cdef:
            Py_ssize_t i
            Py_ssize_t len_keys=mykeys.size()
        for i in range(len_keys):
            try:
                self.c_dict[<string>mykeys[i]]=<string>myvalues[i]
            except Exception:
                if config_settings.debug_enabled:
                    errwrite()
        return 0

    def __getitem__(self, key,/):
        return self.c_dict[key]

    def __setitem__(self, i, item) -> None:
        self.c_dict[i]=item

    def __str__(self) -> str:
        return pformat(dict(self.c_dict),indent=4, width=80,compact=False)

    def __repr__(self) -> str:
        return self.__str__()

    def __delitem__(self, i):
        cdef:
            bint delete_first = False
            bint delete_second = False
            string dictkey = b''
            string dictvalue =b''
            list[bytes] dictvalues=[]
            Py_ssize_t valiter
            strmap.iterator it_start, it_end
        if isinstance(i,tuple):
            delete_first=True
            delete_second=True
            dictkey=i[0]
            dictvalue=i[1]
        elif isinstance(i,bytes):
            delete_first=True
            delete_second=False
            dictkey=i
        elif isinstance(i,list):
            delete_first=False
            delete_second=True
            dictvalues=i
        it_start = self.c_dict.begin()
        it_end = self.c_dict.end()
        while it_start != it_end:
            try:
                defa=deref(it_start)
                if delete_first and delete_second:
                    if (defa.first == dictkey) and (defa.second == dictvalue):
                        self.c_dict.erase(it_start)
                elif delete_first:
                    if (defa.first == dictkey):
                        self.c_dict.erase(it_start)
                        break
                elif delete_second:
                    for valiter in range(len(dictvalues)):
                        if (defa.second == <string>dictvalues[valiter]):
                            self.c_dict.erase(it_start)
                inc(it_start)
            except Exception:
                if config_settings.debug_enabled:
                    errwrite()
    cpdef int do_when_match(self, object filter_function, string myregex_keys,string myregex_values,int regex_flags_keys=0,int regex_flags_values=0):
        cdef:
            strmap.iterator it_start = self.c_dict.begin()
            strmap.iterator it_end = self.c_dict.end()
            string firststring, secondstring
            int returnresult
        while it_start != it_end:
            try:
                defa=deref(it_start)
                firststring=defa.first
                secondstring=defa.second
                returnresult=filter_function(key=firststring,value=secondstring,myregex_keys=myregex_keys,myregex_values=myregex_values,regex_flags_keys=regex_flags_keys,regex_flags_values=regex_flags_values)
                if returnresult==1:
                    return  returnresult
                inc(it_start)
            except Exception:
                if config_settings.debug_enabled:
                    errwrite()
        return 0


def start_subproc(adb_exe='',device_serial='',device_shell='', uiautomator_cmd=b'uiautomator events'):
    r"""
    Starts a subprocess that executes the `uiautomator` command using the Android Debug Bridge (ADB)
    executable specified by the user. This function is designed to be run as a target of a thread for
    asynchronous operation.

    Parameters:
        adb_exe (str): The path to the ADB executable.
        device_serial (str): The serial number of the target device (for ADB commands).
        device_shell (str): The shell command to execute (default is 'sh').
        uiautomator_cmd (bytes): The command to send to uiautomator, typically to trigger event monitoring.

    Effects:
        This function modifies global configurations and appends to the running_uiautomators list to track subprocesses.
    """    
    cdef:
        list[str] adb_commando=[]
    if adb_exe:
        adb_commando.append(adb_exe)
    if device_serial:
        adb_commando.append('-s')
        adb_commando.append(device_serial)
    if device_shell:
        adb_commando.append(device_shell)
    else:
        adb_commando.append('sh')

    obsproc = subprocess.Popen(
        adb_commando,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    )
    config_settings.running_uiautomators.append(obsproc)
    obsproc.stdin.write(uiautomator_cmd + b'\n\n')
    obsproc.stdin.flush()
    obsproc.stdin.close()
    try:
        for line in iter(obsproc.stdout.readline, b""):
            if not config_settings.read_events_data:
                break
            my_parsing_queue.push(line)
    except:
        pass
my_parsing_queue.push(b'')

def start_thread(adb_exe='',device_serial='',device_shell='shell',uiautomator_cmd=b'uiautomator events',thread_daemon=True):
    r"""
    Initializes and starts a thread that runs a subprocess for capturing UI Automator events.
    This function is a higher-level wrapper intended to facilitate threading of the `start_subproc` function.

    Parameters:
        adb_exe (str): The path to the ADB executable.
        device_serial (str): The device serial number to target with ADB.
        device_shell (str): The shell to use in the device, defaults to 'shell'.
        uiautomator_cmd (bytes): The command for UI Automator to execute.
        thread_daemon (bool): Whether the thread should be a daemon.

    Returns:
        threading.Thread: The thread that was started.
    """
    t=threading.Thread(target=start_subproc,kwargs={'adb_exe':adb_exe,'device_serial':device_serial,'device_shell':device_shell, 'uiautomator_cmd':uiautomator_cmd},daemon=thread_daemon)
    t.start()
    return t


def start_parsing(
    string myregex_keys,
    string myregex_values,
    object filter_function=None,
    int regex_flags_keys=re.IGNORECASE,
    int regex_flags_values=re.IGNORECASE,
    float sleep_between_each_scan=0.001,
    bint print_results=True,
    bint regex_nogil=True,
    str device_serial = "",
    str adb_exe = '',
    str device_shell = "shell",
    bytes uiautomator_cmd = b"uiautomator events",
    float sleep_after_starting_thread = 5,
    bint thread_daemon = True,
    bytes uiautomator_kill_cmd=b'pkill uiautomator',
    bint observe_results=False
):
    """
    Coordinates the parsing of UI Automator events by initiating a thread to gather data and then processing that data using regex matching based on user-specified criteria. This function aims to facilitate real-time event handling for UI analysis.

    Parameters:
        myregex_keys (str): Regex pattern to match keys.
        myregex_values (str): Regex pattern to match values.
        filter_function (callable, optional): A function to apply as a filter for matched regex patterns. Should return 1 to stop parsing.
        regex_flags_keys (int): Regex flags for key matching.
        regex_flags_values (int): Regex flags for value matching.
        sleep_between_each_scan (float): Time to wait between each scan loop.
        print_results (bool): Flag to determine whether to print the results.
        regex_nogil (bool): Flag to enable or disable GIL during regex operations.
        device_serial (str), adb_exe (str), device_shell (str), uiautomator_cmd (bytes): Parameters for the thread and subprocess.
        sleep_after_starting_thread (float): Time to wait after starting the thread before processing.
        thread_daemon (bool): Whether the thread should run as a daemon.
        uiautomator_kill_cmd (bytes): Command to kill the uiautomator process.
        observe_results (bool): Whether to observe and react to the results in real-time.

    Notes:
        This function leverages threading and subprocess management to maintain continuous monitoring and processing of UI events.

    Example:
        import regex as re
        import cythonevparser
        import shutil
        cythonevparser.evparse.config_settings.debug_enabled = False

        def filter_keys_function(
            key=b"",
            value=b"",
            myregex_keys=b"",
            myregex_values=b"",
            regex_flags_keys=0,
            regex_flags_values=0,
        ):
            # print('observing')
            try:
                if b"Metallica" in value:
                    return 1

                if re.search(myregex_keys, key, flags=regex_flags_keys) and re.search(
                    myregex_values, value, flags=regex_flags_values
                ):
                    print(key, value)
                    return 1 # stops the loop
                return 0
            except Exception:
                return 0


        device_serial = "127.0.0.1:5560"
        adb_exe = shutil.which("adb")
        device_shell = "shell"
        uiautomator_cmd = b"uiautomator events"
        regex_nogil = True
        sleep_after_starting_thread = 5
        thread_daemon = True
        print_results = True
        sleep_between_each_scan = 0.001
        regex_flags_keys = re.IGNORECASE
        regex_flags_values = re.IGNORECASE
        filter_function = filter_keys_function
        myregex_keys = b"Text|Content"
        myregex_values = rb"Metallica"
        uiautomator_kill_cmd = b"pkill uiautomator"
        observe_results = True


        cythonevparser.evparse.start_parsing(
            myregex_keys=myregex_keys,
            myregex_values=myregex_values,
            filter_function=filter_function,
            regex_flags_keys=regex_flags_keys,
            regex_flags_values=regex_flags_values,
            sleep_between_each_scan=sleep_between_each_scan,
            print_results=print_results,
            regex_nogil=regex_nogil,
            device_serial=device_serial,
            adb_exe=adb_exe,
            device_shell=device_shell,
            uiautomator_cmd=uiautomator_cmd,
            sleep_after_starting_thread=sleep_after_starting_thread,
            thread_daemon=thread_daemon,
            uiautomator_kill_cmd=uiautomator_kill_cmd,
            observe_results=observe_results,
        )

        """
    cdef:
        list[str] adb_commando_kill=[]
        MyDict parsingdict = MyDict()
        stringvector fillkeys=sorted([<string>bv for bv in all_categories_eventparser+(b'TimeNow',)])
        stringvector dummykeys=[<string>b'' for _ in range(len(fillkeys))]
        Py_ssize_t start, end, coun
        list firstfilelds, myke_myva
        dict kwargs_for_observer_function={
        'filter_function':filter_function,
        'myregex_keys':myregex_keys,
        'myregex_values':myregex_values,
        'regex_flags_keys':regex_flags_keys,
        'regex_flags_values':regex_flags_values
        }
        Py_ssize_t print_counter=0
        openmp.omp_lock_t locker
        bytes strax, hxq
        object categories_regex=re.compile(rb"\L<options>", options=all_categories_eventparser, ignore_unused=True)

    t=start_thread(adb_exe=adb_exe if adb_exe else '',device_serial=device_serial,device_shell=device_shell,uiautomator_cmd=uiautomator_cmd,thread_daemon=thread_daemon)
    time.sleep(sleep_after_starting_thread)

    parsingdict.add_values(mykeys=fillkeys, myvalues=dummykeys)
    while not config_settings.running_uiautomators:
        time.sleep(1)
    config_settings.read_events_data=True
    openmp.omp_init_lock(&locker)
    openmp.omp_set_lock(&locker)
    while not my_parsing_queue.empty():
        my_parsing_queue.pop()
    openmp.omp_unset_lock(&locker)
    config_settings.stop=False
    try:
        while not config_settings.stop:
            try:
                time.sleep(sleep_between_each_scan)
                openmp.omp_set_lock(&locker)
                while not my_parsing_queue.empty():
                    if config_settings.stop:
                        break
                    try:
                        start=0
                        end=0
                        coun=0
                        for resu in categories_regex.finditer(hxq:=my_parsing_queue.front(),concurrent=regex_nogil):
                            if config_settings.stop:
                                break
                            try:
                                if coun==0:
                                    firstfilelds=hxq.split(maxsplit=2)
                                    if len(firstfilelds)==3:
                                        parsingdict.c_dict[b'TimeNow']= firstfilelds[1]
                                    coun+=1
                                    continue
                                end=resu.start()
                                strax=(hxq[start:end])
                                if coun!=1:
                                    myke_myva=re.split(br':\s+', strax.rstrip(b'; '),maxsplit=1,)
                                    if len(myke_myva)==2:
                                        parsingdict.c_dict[<string>myke_myva[0]]=<string>myke_myva[1]
                                start=end
                                coun+=1
                            except Exception:
                                if config_settings.debug_enabled:
                                    errwrite()
                        my_parsing_queue.pop()
                        if observe_results:
                            stop_or_continue = parsingdict.do_when_match(**kwargs_for_observer_function)
                            if stop_or_continue==1:
                                config_settings.read_events_data=False
                                config_settings.stop=True
                                break
                        if print_results:
                            print_counter+=1
                            print(parsingdict)
                            print(f'{print_counter} >>>>---------------------------------------------------------')
                        parsingdict.c_dict.clear()
                        parsingdict.add_values(mykeys=fillkeys, myvalues=dummykeys)
                    except Exception:
                        if config_settings.debug_enabled:
                            errwrite()
            except Exception:
                if config_settings.debug_enabled:
                    errwrite()
            finally:
                try:
                    openmp.omp_unset_lock(&locker)
                except Exception:
                    if config_settings.debug_enabled:
                        errwrite()
    except Exception:
        pass
    except KeyboardInterrupt:
        try:
            openmp.omp_unset_lock(&locker)
        except:
            if config_settings.debug_enabled:
                errwrite()
        try:
            print('Shutting down...')
            config_settings.stop=True
            config_settings.read_events_data=False
            time.sleep(0.001)
        except:
            pass
    if adb_exe:
        adb_commando_kill.append(adb_exe)
    if device_serial:
        adb_commando_kill.append('-s')
        adb_commando_kill.append(device_serial)
    if device_shell:
        adb_commando_kill.append(device_shell)
    else:
        adb_commando_kill.append('sh')
    killsubproc=subprocess.Popen(
            adb_commando_kill,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
        )
    killsubproc.stdin.write(uiautomator_kill_cmd + b'\n\n')
    killsubproc.stdin.flush()
    killsubproc.stdin.close()
    try:
        killthread(t)
    except Exception:
            errwrite()
    try:
        openmp.omp_destroy_lock(&locker)
    except Exception:
        if config_settings.debug_enabled:
            errwrite()
    for subpro in config_settings.running_uiautomators:
        try:
            subpro.kill()
        except Exception:
            pass
    config_settings.running_uiautomators.clear()
    config_settings.read_events_data=True
    config_settings.stop=False
    try:
        killsubproc.kill()
    except Exception:
        if config_settings.debug_enabled:
            errwrite()



