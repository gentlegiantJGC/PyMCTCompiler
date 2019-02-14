^+b::
clipboard =  ;
Send ^c
ClipWait  ;
ToolTip % clipboard
sleep 500
ToolTip
f = numerical.button_bedrock("minecraft", "%clipboard%")
FileDelete, %A_MyDocuments%\GitHub\Minecraft-Universal-Block-Mappings\Primitives\numerical\bedrock\vanilla\button\bedrock_%clipboard%.pyjson
FileAppend %f%, %A_MyDocuments%\GitHub\Minecraft-Universal-Block-Mappings\Primitives\numerical\bedrock\vanilla\button\bedrock_%clipboard%.pyjson
Send {Right}+{End}{Backspace}":{Space}"bedrock_%clipboard%"
Return