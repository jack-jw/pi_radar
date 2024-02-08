scriptDir=$(dirname "$0")

cd "$scriptDir"
echo "Compiling $scriptDir/client.applescript to $scriptDir/Pi-radar.app/Contents/Resources/Scripts/main.scpt"
osacompile -x -o "$scriptDir/Pi-radar.app/Contents/Resources/Scripts/main.scpt" "$scriptDir/client.applescript"
open -a "$scriptDir/Pi-radar.app"