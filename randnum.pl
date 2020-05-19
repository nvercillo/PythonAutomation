#!/usr/bin/perl
open (OVERWRITE, ">rand.txt") or die "$! You deleted random number file! Make a new one (rand.txt)!!!!!!!";;
$circle=int(rand(23) +9);
print OVERWRITE $circle;