^+t::
clipboard =  ;
Send ^c
ClipWait  ;
sleep 500
f = numerical.glazed_terracotta("minecraft", "%clipboard%", "%clipboard%", "minecraft", "glazed_terracotta")
FileDelete, %A_MyDocuments%\GitHub\Minecraft-Universal-Block-Mappings\Primitives\numerical\bedrock\vanilla\glazed_terracotta\%clipboard%.pyjson
FileAppend %f%, %A_MyDocuments%\GitHub\Minecraft-Universal-Block-Mappings\Primitives\numerical\bedrock\vanilla\glazed_terracotta\%clipboard%.pyjson
Send {Right}+{End}{Backspace}":{Space}"%clipboard%"
Return