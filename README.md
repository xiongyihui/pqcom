![pqcom](img/pqcom-logo-expanded.png)
====

A simple serial tool for Linux/Windows/Mac. It's written by Python and Qt (PySide).

```
+------------------------------------------------------------------+
| pq                      pqcom                             O - X  |
+------------------------------------------------------------------+
| + | > | = | H | X | i |                                          |
+------------------------------------------------------------------+
| |   |   |   |   |   |                                            |
| |   |   |   |   |   +---> Open about dialog                      |
| |   |   |   |   |                                                |
| |   |   |   |   +-------> Clear received message                 |
| |   |   |   |                                                    |
| |   |   |   +-----------> Enable/Disable Hex View                |
| |   |   |                                                        |
| |   |   +---------------> Open settings dialog                   |
| |   |                                                            |
| |   +-------------------> Open/Close serial port                 |
| |                                                                |
| +-----------------------> Open a new window                      |
|                                                                  |
|                                                                  |
|                                                                  |
+------------------------------------------------------------------+
|                                                                  |
|  Keyboard Shortcut                                               |
|                                                                  |
|      Ctrl + Enter: Send                                          |
|                                                                  |
|                                                                  |
+------------------------------------------------------------------+
| + Normal | O Hex | O Extend | * | History |    | # Repeat | Send |
+------------------------------------------------------------------+
```

### Requirements

-	python
-	pyserial
-	pyside

### Usage

-	Linux/Mac

	```
	pip install pyserial
	pip install pyside
	git clone https://github.com/xiongyihui/pqcom.git
	python pqcom/pqcom.py
	```

-	Windows

	Go to [release channel](https://github.com/xiongyihui/pqcom/releases) and download executable application.
    
The icons are from [KDE Plasma Breeze Icons](https://github.com/NitruxSA/plasma-next-icons/)
    
![pqcom](preview/pqcom.png)
