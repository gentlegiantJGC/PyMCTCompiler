execute @a[scores={t=2}] ~ ~ ~ fill ~ ~-2 ~ ~2 ~-2 ~16 chest
tp @a[scores={t=..45}] ~ ~1 ~
execute @a[scores={t=41}] ~ ~ ~ function education/allow
execute @a[scores={t=42}] ~ ~ ~ function education/border_block
execute @a[scores={t=43}] ~ ~ ~ function education/camera
execute @a[scores={t=44}] ~ ~ ~ function education/chalkboard
execute @a[scores={t=45}] ~ ~ ~ function education/deny
scoreboard players add @a t 1