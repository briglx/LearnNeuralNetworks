param(
 [string]
 $Cloud = "Public",
 [string]
 $FileName = ""
)
####### Download json file  ############
$downloadUri = 'https://www.microsoft.com/en-us/download/confirmation.aspx?id=56519'
if( $Cloud -eq "USGov" ) {
	$downloadUri = 'https://www.microsoft.com/en-us/download/confirmation.aspx?id=57063'
} elseif( $Cloud -eq "Germany" ) {
	$downloadUri = 'https://www.microsoft.com/en-us/download/confirmation.aspx?id=57064'
} elseif( $Cloud -eq "China" ) {
	$downloadUri = 'https://www.microsoft.com/en-us/download/confirmation.aspx?id=57062'
}
$downloadPage = Invoke-WebRequest -Uri $downloadUri
$jsonFileUri = ($downloadPage.RawContent.Split('"') -like "https://*ServiceTags*")[0]
if( $FileName -eq "" ) {
	$NameParts = $jsonFileUri.Split('/')
	if ( -Not (Test-Path "$PSScriptRoot\downloads") ) {
		New-Item -Path "$PSScriptRoot\downloads" -ItemType directory
	}
	$FileName = "$PSScriptRoot\downloads\$($NameParts[ $NameParts.Count - 1 ])"
} 
(New-Object System.Net.WebClient).DownloadFile($jsonFileUri, $FileName)
$FileName