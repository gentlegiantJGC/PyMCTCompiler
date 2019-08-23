^+f::
clipboard =  ;
Send ^c
ClipWait  ;
sleep 500
f = numerical.fence_gate("minecraft", "%clipboard%", "%clipboard%", "minecraft", "fence_gate")
FileDelete, %A_MyDocuments%\GitHub\Minecraft-Universal-Block-Mappings\Primitives\numerical\bedrock\vanilla\fence_gate\%clipboard%.pyjson
FileAppend %f%, %A_MyDocuments%\GitHub\Minecraft-Universal-Block-Mappings\Primitives\numerical\bedrock\vanilla\fence_gate\%clipboard%.pyjson
Send {Right}+{End}{Backspace}":{Space}"%clipboard%"
Return