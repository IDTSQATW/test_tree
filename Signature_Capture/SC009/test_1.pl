#!/usr/bin/perl

# Using Packages
use Env;
use Cwd;

# Defining Global Variables
$start_dir = &cwd();
$verbose = 1;

# Parsing Command Line
for(;;)						# forever loop
{
    last if($#ARGV < 0);
    $argv = shift(@ARGV);
    if(($argv eq "-h") ||
       ($argv eq "-help") ||
       ($argv eq "-?"))
    {
        printf("This program does an example test on the DockLight\n");
	printf("Options:\n");
	printf(" -h[elp]/-?             print this help blurb\n");
	printf(" -v N                   set verbosity to N\n");
        exit 1;
    }
    if(($argv eq "-v"))        { $verbose = shift(@ARGV); next; }

}						# end forever

`start /REALTIME docklight_scripting -r -m SC009.pts`;

# Main Code



# Exit
exit 0;
