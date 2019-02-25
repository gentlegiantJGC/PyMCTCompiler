^+w::
clipboard =  ;
Send ^c
ClipWait  ;
ToolTip % clipboard
sleep 1000
ToolTip
f = numerical.pressure_plate("minecraft", "%clipboard%", "%clipboard%")
FileDelete, %A_MyDocuments%\GitHub\Minecraft-Universal-Block-Mappings\Primitives\numerical\bedrock\vanilla\pressure_plate\%clipboard%.pyjson
FileAppend %f%, %A_MyDocuments%\GitHub\Minecraft-Universal-Block-Mappings\Primitives\numerical\bedrock\vanilla\pressure_plate\%clipboard%.pyjson
Send {Right}+{End}{Backspace}":{Space}"%clipboard%"
Return