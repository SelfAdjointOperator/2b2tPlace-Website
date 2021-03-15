function Path-From-Invocation {
    param (
        $child
    )
    return $(Join-Path -Path $(Split-Path -Parent ($PSCommandPath)) -ChildPath $child -Resolve)
}

$srcReactBuildPath = $(Path-From-Invocation "build")

$rootPath = $(Path-From-Invocation "../src/MyFlaskModules/root")

$tmpCWD = $pwd
cd $srcReactBuildPath
npm run build

rm "$rootPath\templates\root\index.html" -ErrorAction SilentlyContinue
rm "$rootPath\static\js\*"
rm "$rootPath\static\css\*"

mv "$srcReactBuildPath\index.html" "$rootPath\templates\root\index.html"
mv "$srcReactBuildPath\static\js\*" "$rootPath\static\js\"
mv "$srcReactBuildPath\static\css\*" "$rootPath\static\css\"

cd $tmpCWD
