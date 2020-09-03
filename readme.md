CH101 Zoom Attendance Check Parser
===

Installation
---

1. Install Python3
2. Download this repo

Usage
---

1. Get a access to terminal in your environment.

    For example, in Windows, powershell will work.

    For MacOS and Unix-like OS, use terminal emulator.

2. Execute the main module with python in commandline as follows. You must give target txt file path as argument.

    ```
    # goto root folder of this project

    $ python3 main.py <input txt file name>
    ```

    You may need to move txt file in appropriate directory.

    ```
    # example: Place "zoom_log.txt" in "input" directory

    $ python3 main.py input/zoom_log.txt
    ```

3. The parsed result will be in `output` directory.

    `check_output.csv` contains attendance check result, by student ID, name, and 'O' or 'X' indicating validity.

    `error_output.csv` contains the lines that program was not able to parse. You may use it for manual checking.

Caveats
---

1. The program assumes following format for attendance checking chat.

    ```
    # format

    Time         시작  <Zoom username> : <ID> <Name>

    # example

    12:00:00	 시작  20201234_홍길동 : 20201234 홍길동
    ```

2. Two chat before 13:10 and 14:00 are needed to mark attendance check.

3. If two usernames used in check before 13:10 and after 14:00 does not match, program marks it as invalid attendance check.

    ```
    # example where program marks as invalid check

    13:00:00	 시작  20201234_홍길동 : 20201234 홍길동

    ...
    
    14:10:00	 시작  길동 홍 : 20201234 홍길동
    ```

Credit
---

Yusung Sim

yusungsim@github.com