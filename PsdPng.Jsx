var inputFolder = Folder.selectDialog("Escolha a pasta com os arquivos PSD");
var outputFolder = Folder.selectDialog("Escolha a pasta para salvar os PNGs");

if (inputFolder != null && outputFolder != null) {
    var files = inputFolder.getFiles("*.psd");

    for (var i = 0; i < files.length; i++) {
        var doc = open(files[i]);

        var options = new PNGSaveOptions();
        var fileName = decodeURI(doc.name).replace(".psd", ".png");
        var saveFile = new File(outputFolder + "/" + fileName);

        doc.saveAs(saveFile, options, true, Extension.LOWERCASE);
        doc.close(SaveOptions.DONOTSAVECHANGES);
    }

    alert("Exportação concluída!");
}
