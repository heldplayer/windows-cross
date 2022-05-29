# Your First Windows Program

This sample is based on the code from Microsoft at https://docs.microsoft.com/en-us/windows/win32/learnwin32/your-first-windows-program and https://github.com/microsoft/Windows-classic-samples/tree/main/Samples/Win7Samples/begin/LearnWin32/HelloWorld.

It is modified slightly to be a basic but properly functioning Win32 app.

The following changes were done:
- Set `wc.hCursor` to `LoadCursorW(NULL, IDC_ARROW)` when defining the window, as it would otherwise never properly set the mouse cursor.
- Set `wc.hbrBackground` to `(HBRUSH)(COLOR_WINDOW + 1)` when defining the window, and removed the `WM_PAINT` case from the `WindowProc`, as we're only interested in having a minimal functional sample.
