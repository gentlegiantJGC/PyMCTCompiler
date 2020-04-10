execute @a[scores={t=2}] ~ ~ ~ fill ~ ~-2 ~ ~2 ~-2 ~16 chest
tp @a[scores={t=..44}] ~ ~1 ~
execute @a[scores={t=41}] ~ ~ ~ function vanilla_1.14/bee_nest
execute @a[scores={t=42}] ~ ~ ~ function vanilla_1.14/beehive
execute @a[scores={t=43}] ~ ~ ~ function vanilla_1.14/honey_block
execute @a[scores={t=44}] ~ ~ ~ function vanilla_1.14/honeycomb_block
scoreboard players add @a t 1