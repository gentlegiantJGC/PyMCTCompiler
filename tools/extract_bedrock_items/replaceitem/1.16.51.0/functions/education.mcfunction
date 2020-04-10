execute @a[scores={t=2}] ~ ~ ~ fill ~ ~-2 ~ ~2 ~-2 ~16 chest
tp @a[scores={t=..42}] ~ ~1 ~
execute @a[scores={t=41}] ~ ~ ~ function education/camera
execute @a[scores={t=42}] ~ ~ ~ function education/chalkboard
scoreboard players add @a t 1