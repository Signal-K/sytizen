```bash
api wb3-14--generate-asset-id-statselements-for*​​​ ≡2m43s 
.venv ❯ flask run
 * Tip: There are .env or .flaskenv files present. Do "pip install python-dotenv" to use them.
[{'id': 2, 'created_at': '2022-10-22T16:02:02.252739+00:00', 'title': 'Venus', 'Owner': None, 'Star': None}, {'id': 3, 'created_at': '2022-10-22T16:02:10.566645+00:00', 'title': 'Earth', 'Owner': None, 'Star': None}, {'id': 5, 'created_at': '2022-11-09T18:25:05.147101+00:00', 'title': 'Jupiter', 'Owner': None, 'Star': None}, {'id': 6, 'created_at': '2022-11-09T18:37:44.09209+00:00', 'title': 'Saturn', 'Owner': None, 'Star': None}, {'id': 7, 'created_at': '2022-11-09T18:39:09.364099+00:00', 'title': 'Uranus', 'Owner': None, 'Star': None}, {'id': 4, 'created_at': '2022-11-09T18:21:28.573826+00:00', 'title': 'Mars', 'Owner': None, 'Star': None}, {'id': 1, 'created_at': '2022-10-22T16:01:50.919142+00:00', 'title': 'Mercury', 'Owner': None, 'Star': 'Sol'}]
 * Debug mode: off
2023-03-17 15:29:53,067:INFO - WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
2023-03-17 15:29:53,067:INFO - Press CTRL+C to quit
 80%|███████████████████████████████████████████████████████████▎              | 1641/2048 [00:44<00:12, 33.19it/s]2023-03-17 15:30:39,990:INFO - 127.0.0.1 - - [17/Mar/2023 15:30:39] "POST /get_image HTTP/1.1" 405 -
 89%|█████████████████████████████████████████████████████████████████▋        | 1817/2048 [00:49<00:06, 38.21it/s]2023-03-17 15:30:44,835:INFO - 127.0.0.1 - - [17/Mar/2023 15:30:44] "GET /get_image HTTP/1.1" 200 -
100%|██████████████████████████████████████████████████████████████████████████| 2048/2048 [00:50<00:00, 40.26it/s]
/Users/buyer/Documents/Lens/client/api/main.py:189: UserWarning: Starting a Matplotlib GUI outside of the main thread will likely fail.
  plt.axis("off")
2023-03-17 15:30:47.231 Python[36347:3099950] *** Terminating app due to uncaught exception 'NSInternalInconsistencyException', reason: 'NSWindow drag regions should only be invalidated on the Main Thread!'
*** First throw call stack:
(
        0   CoreFoundation                      0x00000001c55ac1dc __exceptionPreprocess + 240
        1   libobjc.A.dylib                     0x00000001c52fd808 objc_exception_throw + 60
        2   CoreFoundation                      0x00000001c55d6e20 _CFBundleGetValueForInfoKey + 0
        3   AppKit                              0x00000001c809b15c -[NSWindow(NSWindow_Theme) _postWindowNeedsToResetDragMarginsUnlessPostingDisabled] + 380
        4   AppKit                              0x00000001c8085f20 -[NSWindow _initContent:styleMask:backing:defer:contentView:] + 948
        5   AppKit                              0x00000001c8085b60 -[NSWindow initWithContentRect:styleMask:backing:defer:] + 56
        6   _macosx.cpython-310-darwin.so       0x000000010bd909d8 -[Window initWithContentRect:styleMask:backing:defer:withManager:] + 52
        7   _macosx.cpython-310-darwin.so       0x000000010bd93c14 FigureManager_init + 224
        8   Python                              0x0000000105422e18 wrap_init + 20
        9   Python                              0x00000001053b7c00 wrapperdescr_call + 400
        10  Python                              0x00000001053acfb4 _PyObject_MakeTpCall + 136
        11  Python                              0x00000001054a6d08 call_function + 272
        12  Python                              0x00000001054a4490 _PyEval_EvalFrameDefault + 42884
        13  Python                              0x0000000105498aac _PyEval_Vector + 376
        14  Python                              0x00000001053ad21c _PyObject_FastCallDictTstate + 96
        15  Python                              0x0000000105422c48 slot_tp_init + 196
        16  Python                              0x000000010541ac10 type_call + 288
        17  Python                              0x00000001053acfb4 _PyObject_MakeTpCall + 136
        18  Python                              0x00000001054a6d08 call_function + 272
        19  Python                              0x00000001054a44b8 _PyEval_EvalFrameDefault + 42924
        20  Python                              0x0000000105498aac _PyEval_Vector + 376
        21  Python                              0x00000001053b0218 method_vectorcall + 124
        22  Python                              0x00000001054a6c78 call_function + 128
        23  Python                              0x00000001054a4490 _PyEval_EvalFrameDefault + 42884
        24  Python                              0x0000000105498aac _PyEval_Vector + 376
        25  Python                              0x00000001053b0218 method_vectorcall + 124
        26  Python                              0x00000001054a6c78 call_function + 128
        27  Python                              0x00000001054a4490 _PyEval_EvalFrameDefault + 42884
        28  Python                              0x0000000105498aac _PyEval_Vector + 376
        29  Python                              0x00000001053b0218 method_vectorcall + 124
        30  Python                              0x00000001054a6c78 call_function + 128
        31  Python                              0x00000001054a4490 _PyEval_EvalFrameDefault + 42884
        32  Python                              0x0000000105498aac _PyEval_Vector + 376
        33  Python                              0x00000001053b0218 method_vectorcall + 124
        34  Python                              0x00000001053ad7fc PyVectorcall_Call + 184
        35  Python                              0x00000001054a4658 _PyEval_EvalFrameDefault + 43340
        36  Python                              0x0000000105498aac _PyEval_Vector + 376
        37  Python                              0x00000001053ad7fc PyVectorcall_Call + 184
        38  Python                              0x00000001054a4658 _PyEval_EvalFrameDefault + 43340
        39  Python                              0x0000000105498aac _PyEval_Vector + 376
        40  Python                              0x00000001054a4658 _PyEval_EvalFrameDefault + 43340
        41  Python                              0x0000000105498aac _PyEval_Vector + 376
        42  Python                              0x00000001054a6c78 call_function + 128
        43  Python                              0x00000001054a44b8 _PyEval_EvalFrameDefault + 42924
        44  Python                              0x0000000105498aac _PyEval_Vector + 376
        45  Python                              0x00000001054a6c78 call_function + 128
        46  Python                              0x00000001054a44b8 _PyEval_EvalFrameDefault + 42924
        47  Python                              0x0000000105498aac _PyEval_Vector + 376
        48  Python                              0x00000001054a6c78 call_function + 128
        49  Python                              0x00000001054a44b8 _PyEval_EvalFrameDefault + 42924
        50  Python                              0x0000000105498aac _PyEval_Vector + 376
        51  Python                              0x00000001054a6c78 call_function + 128
        52  Python                              0x00000001054a4490 _PyEval_EvalFrameDefault + 42884
        53  Python                              0x0000000105498aac _PyEval_Vector + 376
        54  Python                              0x00000001054a6c78 call_function + 128
        55  Python                              0x00000001054a44b8 _PyEval_EvalFrameDefault + 42924
        56  Python                              0x0000000105498aac _PyEval_Vector + 376
        57  Python                              0x00000001054a4658 _PyEval_EvalFrameDefault + 43340
        58  Python                              0x0000000105498aac _PyEval_Vector + 376
        59  Python                              0x00000001054a6c78 call_function + 128
        60  Python                              0x00000001054a4418 _PyEval_EvalFrameDefault + 42764
        61  Python                              0x0000000105498aac _PyEval_Vector + 376
        62  Python                              0x00000001054a6c78 call_function + 128
        63  Python                              0x00000001054a4418 _PyEval_EvalFrameDefault + 42764
        64  Python                              0x0000000105498aac _PyEval_Vector + 376
        65  Python                              0x00000001054a6c78 call_function + 128
        66  Python                              0x00000001054a4418 _PyEval_EvalFrameDefault + 42764
        67  Python                              0x0000000105498aac _PyEval_Vector + 376
        68  Python                              0x00000001053ad21c _PyObject_FastCallDictTstate + 96
        69  Python                              0x00000001054218e8 slot_tp_call + 196
        70  Python                              0x00000001053acfb4 _PyObject_MakeTpCall + 136
        71  Python                              0x00000001054a6d08 call_function + 272
        72  Python                              0x00000001054a44b8 _PyEval_EvalFrameDefault + 42924
        73  Python                              0x0000000105498aac _PyEval_Vector + 376
        74  Python                              0x00000001054a6c78 call_function + 128
        75  Python                              0x00000001054a44b8 _PyEval_EvalFrameDefault + 42924
        76  Python                              0x0000000105498aac _PyEval_Vector + 376
        77  Python                              0x00000001053b0218 method_vectorcall + 124
        78  Python                              0x00000001054a6c78 call_function + 128
        79  Python                              0x00000001054a44b8 _PyEval_EvalFrameDefault + 42924
        80  Python                              0x0000000105498aac _PyEval_Vector + 376
        81  Python                              0x00000001053b0218 method_vectorcall + 124
        82  Python                              0x00000001054a6c78 call_function + 128
        83  Python                              0x00000001054a4490 _PyEval_EvalFrameDefault + 42884
        84  Python                              0x0000000105498aac _PyEval_Vector + 376
        85  Python                              0x00000001053b0218 method_vectorcall + 124
        86  Python                              0x00000001054a6c78 call_function + 128
        87  Python                              0x00000001054a4490 _PyEval_EvalFrameDefault + 42884
        88  Python                              0x0000000105498aac _PyEval_Vector + 376
        89  Python                              0x00000001053b0218 method_vectorcall + 124
        90  Python                              0x00000001054a6c78 call_function + 128
        91  Python                              0x00000001054a4490 _PyEval_EvalFrameDefault + 42884
        92  Python                              0x0000000105498aac _PyEval_Vector + 376
        93  Python                              0x00000001053ad21c _PyObject_FastCallDictTstate + 96
        94  Python                              0x0000000105422c48 slot_tp_init + 196
        95  Python                              0x000000010541ac10 type_call + 288
        96  Python                              0x00000001053acfb4 _PyObject_MakeTpCall + 136
        97  Python                              0x00000001054a6d08 call_function + 272
        98  Python                              0x00000001054a4490 _PyEval_EvalFrameDefault + 42884
        99  Python                              0x0000000105498aac _PyEval_Vector + 376
        100 Python                              0x00000001054a6c78 call_function + 128
        101 Python                              0x00000001054a4418 _PyEval_EvalFrameDefault + 42764
        102 Python                              0x0000000105498aac _PyEval_Vector + 376
        103 Python                              0x00000001053b02bc method_vectorcall + 288
        104 Python                              0x00000001054a4658 _PyEval_EvalFrameDefault + 43340
        105 Python                              0x0000000105498aac _PyEval_Vector + 376
        106 Python                              0x00000001054a6c78 call_function + 128
        107 Python                              0x00000001054a4418 _PyEval_EvalFrameDefault + 42764
        108 Python                              0x0000000105498aac _PyEval_Vector + 376
        109 Python                              0x00000001054a6c78 call_function + 128
        110 Python                              0x00000001054a4418 _PyEval_EvalFrameDefault + 42764
        111 Python                              0x0000000105498aac _PyEval_Vector + 376
        112 Python                              0x00000001053b0320 method_vectorcall + 388
        113 Python                              0x0000000105564c74 thread_run + 120
        114 Python                              0x0000000105503bd4 pythread_wrapper + 48
        115 libsystem_pthread.dylib             0x00000001c54614ec _pthread_start + 148
        116 libsystem_pthread.dylib             0x00000001c545c2d0 thread_start + 8
)
libc++abi: terminating with uncaught exception of type NSException
zsh: abort      flask run
/opt/homebrew/Cellar/python@3.10/3.10.9/Frameworks/Python.framework/Versions/3.10/lib/python3.10/multiprocessing/resource_tracker.py:224: UserWarning: resource_tracker: There appear to be 1 leaked semaphore objects to clean up at shutdown
  warnings.warn('resource_tracker: There appear to be %d '
```

This is when running the flask app `app.py`. Going to the index route on Insominia results in a timeout because the generator is busy, so we should move the generator into the `send_image` route. The generated image is being sent as a request, now all that's left to do is lazy mint that, grab the image, and send that and the contract info into Supabase.