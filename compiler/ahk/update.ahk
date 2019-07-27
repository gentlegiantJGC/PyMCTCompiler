^+u::
clipboard =  ;
Send ^x
ClipWait  ;
sleep 10
split_clip := StrSplit(clipboard, ":", "", 2)

fun_name := split_clip[1]
clipboard := split_clip[2]

Send {{}{Enter}"function":
SendRaw %fun_name%
Send, ,{Enter}"options": ^v
Return