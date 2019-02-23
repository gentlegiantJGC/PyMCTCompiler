^+w::
clipboard =  ;
Send ^c
ClipWait  ;
ToolTip % clipboard
sleep 1000
ToolTip
f = numerical.stripped_log("minecraft", "%clipboard%", "%clipboard%")
FileDelete, %A_MyDocuments%\GitHub\Minecraft-Universal-Block-Mappings\Primitives\numerical\bedrock\vanilla\log\%clipboard%.pyjson
FileAppend %f%, %A_MyDocuments%\GitHub\Minecraft-Universal-Block-Mappings\Primitives\numerical\bedrock\vanilla\log\%clipboard%.pyjson
Send {Right}+{End}{Backspace}":{Space}"%clipboard%"
Return