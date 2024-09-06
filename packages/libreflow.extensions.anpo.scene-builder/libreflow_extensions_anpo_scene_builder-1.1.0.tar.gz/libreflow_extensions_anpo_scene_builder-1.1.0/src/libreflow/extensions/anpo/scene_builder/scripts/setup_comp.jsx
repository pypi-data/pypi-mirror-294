#target AfterEffects

// ----- Utils
function print(msg) {
    $.writeln(msg)
}
$.print = print;

/*
  Modification de l'objet string pour ajouter les fonctions endsWith et startsWith
*/

String.prototype.endsWith = function(suffix) {
    return this.indexOf(suffix, this.length - suffix.length) !== -1;
};

String.prototype.startsWith = function(prefix) {
    return this.indexOf(prefix, 0) !== -1;
};

function findItemsByName (name) {
    var items = [];
    for (var i = 0; i < app.project.numItems; i++) {
        var item = app.project.items[i+1];
        if (item.name.match(new RegExp(name.replace(/_/g, "[- _]")))
            && item instanceof FootageItem) {
            items.push(item);
        }
    }
    return items;
}

function getLatestVersion (versionsPath) {
    var versionsDir = new Folder(versionsPath);
    if (!versionsDir.exists) {
        return null;
    }

    var versions = versionsDir.getFiles("v???");

    // Get latest version
    if (versions.length)
    {
        return versions[versions.length - 1];
    }
    return null;
}

function getPassesDir () {
    var passesDir = "/c/projets/anpo/anpo/sq{sq}/sh{sh}/comp/passes";
    passesDir = passesDir.replace(/{sq}/g, sq);
    passesDir = passesDir.replace(/{sh}/g, sh);
    return new Folder(passesDir);
}

// FROM Smart Import.jx
function testForSequence (files) {
    var searcher = new RegExp("[0-9]+");
    var movieFileSearcher = new RegExp("(mov|avi|mpg)$", "i");
    var parseResults = new Array;

    // Test that we have a sequence. Stop parsing after 10 files.
    for (x = 0; (x < files.length) & x < 10; x++) {
        var movieFileResult = movieFileSearcher.exec(files[x].name);
        if (!movieFileResult) {
            var currentResult = searcher.exec(files[x].name);
            // Regular expressions return null if no match was found.
            // Otherwise, they return an array with the following information:
            // array[0] = the matched string.
            // array[1..n] = the matched capturing parentheses.

            if (currentResult) { // We have a match -- the string contains numbers.
                // The match of those numbers is stored in the array[1].
                // Take that number and save it into parseResults.
                parseResults[parseResults.length] = currentResult[0];
            } else {
                parseResults[parseResults.length] = null;
            }
        } else {
            parseResults[parseResults.length] = null;
        }
    }
    // If all the files we just went through have a number in their file names,
    // assume they are part of a sequence and return the first file.

    var result = null;
    for (j = 0; j < parseResults.length; ++j) {
        if (parseResults[j]) {
            if (!result) {
                result = files[j];
            }
        } else {
            // In this case, a file name did not contain a number.
            result = null;
            break;
        }
    }

    return result;
}

function importSafeWithError(importOptions) {
    try {
        return app.project.importFile(importOptions);
    } catch (error) {
        alert(error.toString() + importOptions.file.fsName, scriptName);
    }
}

function cleanupSetLayerName(name) {
    // Find layer index from Blender layer
    var match = name.match(/(?:.*design|sq[0-9a-z]+[-_]bg[0-9]+_?)([0-9]+_.*?)(?:_HI)?$/);

    if (!match) {
        // Typically, a camera, solid, or badly named layer
        return null;
    }
    return match[1];
}

function cleanupPassLayerName(name) {
    var match = name.match(/(?:.*[0-9]+[-_])_([0-9]+_.*?)(?:_HI)?$/);

    if (!match) {
        // Typically, a camera, solid, or badly named layer
        return null;
    }
    return match[1];
}

// -----------------------

app.beginUndoGroup("Import Illustrator file");

// Setup project
// Colour
app.project.bitsPerChannel = 16;
app.project.linearizeWorkingSpace = true;
app.project.workingSpace = 'sRGB IEC61966-2.1';

var bgColor = [0.2, 0.2, 0.2];

// TODO FPS

var AIFileFound = false;

// Get sequence and background number
for (var i = 0; i < app.project.numItems; i++) {
    var item = app.project.items[i+1];
    if (item instanceof FootageItem) {
        if (!item.file) {
            continue;
        }
        var setPath = item.file.fullName;
        var match = setPath.match(/\/sq([0-9a-z]+)-bg([0-9]+)\//);
    if (match == null)
    {
      match = setPath.match(/\/sq([0-9a-z]+)_bg([0-9]+)\//);
    }

        var sq = match[1], bg = match[2];
        if (sq && bg) {
            AIFileFound = true;
        }
    }
    else if (item instanceof CompItem) {
        var blenderComp = item;
    }
}


// List versions in dir
// TODO better handling of drive?
if (AIFileFound) {
    var AIVersionsPath;

    var dirsToTest = ["/c/projets/anpo/lib/sets/sq{sq}/sq{sq}_bg{bg}/design/design_ai/",
                      "/c/projets/anpo/lib/sets/sq{sq}/sq{sq}-bg{bg}/design/design_ai/"];
    for (var i = 0; i < dirsToTest.length; i++) {
        AIVersionsPath = dirsToTest[i];
        AIVersionsPath = AIVersionsPath.replace(/{sq}/g, sq);
        AIVersionsPath = AIVersionsPath.replace(/{bg}/g, bg);
        AIVersion = getLatestVersion(AIVersionsPath);
        if (AIVersion != null) {
            break;
        }
    }
    print("Version: ");
    print(AIVersion);

    // Construct AI file path
    var AIFilePath = AIVersion.fullName+ "/sq{sq}-bg{bg}_design.ai".replace(/{sq}/g, sq).replace(/{bg}/g, bg);
    print("AI File path:");
    print(AIFilePath);

    // Import Illustrator file
    var AI_ImportOptions = new ImportOptions(new File(AIFilePath));
    AI_ImportOptions.importAs = ImportAsType.COMP;
    var AIComp = app.project.importFile(AI_ImportOptions);
}

// Make a precomp from Blender Layers, and add AI layers to their respective precomp
var precompFolder = app.project.items.addFolder("COMP");

for (var i = 0; i < blenderComp.numLayers; i++) {
    var blenderLayer = blenderComp.layers[i+1];

    // Use green labels for nulls
    if (blenderLayer.nullLayer) {
        blenderLayer.label = 9;
    }

    // Find layer index from Blender layer
    var layerName = cleanupSetLayerName(blenderLayer.name);

    if (!layerName) {
        // Typically, a camera, solid, or badly named layer
        continue;
    }

    // Find AI item
    var AIItem = null;
    var foundItems = findItemsByName(layerName);
    for (var j = 0; j < foundItems.length; j++) {
        if (foundItems[j].mainSource.file.name.match(/design.*\.ai$/)) {
            AIItem = foundItems[j];
            break;
        }
    }

    if (AIItem == null) {
        continue;
    }

    // Precomp Blender layer and disable it
    var layerPrecomp = blenderComp.layers.precompose([i+1], layerName, false);
    layerPrecomp.parentFolder = precompFolder;
    layerPrecomp.layers[1].enabled = false;

    // Enable collapseTransformation for the precomp, so that it's continuously rasterized
    layerPrecomp.usedIn[0].layer(layerPrecomp.name).collapseTransformation = false;

    // Get layer from AI comp
    for (var j = 0; j < AIComp.numLayers; j++) {
        if (AIComp.layers[j+1].source == AIItem) {
            var AILayer = AIComp.layers[j+1];
            break;
        }
    }

    // Add AI layer to the precomp
    AILayer.copyToComp(layerPrecomp);

    // Setup layer properties
    layerPrecomp.layer(1).outPoint = blenderLayer.outPoint;
    layerPrecomp.layer(1).collapseTransformation = false;
    layerPrecomp.layer(1).threeDLayer = true;

    layerPrecomp.layer(1).property("position").setValue([0.0,0.0,0.0]);
    layerPrecomp.layer(1).property("anchorPoint").setValue([0.0,0.0,0.0]);
    // Calculate scale as ratio from Blender layer
    var scale = 100.0 * layerPrecomp.layer(2).source.width / layerPrecomp.layer(1).source.width;
    layerPrecomp.layer(1).property("scale").setValue([scale, scale, scale]);

    layerPrecomp.bgColor = bgColor;

    // Enable individual layer but disable precomp if it was disabled in AI file
    if (!AILayer.enabled) {
        layerPrecomp.layer(1).enabled = true;
        layerPrecomp.usedIn[0].layer(layerPrecomp.name).enabled = false;
    }
}

// Rename folders
for (var i = 0; i < app.project.numItems; i++) {
    var item = app.project.items[i+1];
    if (item instanceof FolderItem) {
        // if (item.name.includes("_layers")) {
        if (item.name.match(new RegExp("_layers"))) {
            item.name = "BLENDER_LAYERS";
        }
        else if (item.name.match(new RegExp("Calques"))) {
            item.name = "BG";
        }
        else if (item.name.match(new RegExp("Solides"))) {
            item.name = "Solids";
        }
    }
}

// Rename Blender comp
var match = blenderComp.name.match(/sq([0-9]+).*?sh([0-9]+)/);
var sq = match[1], sh = match[2];
blenderComp.name = "sq" + sq + "_sh" + sh;

// Rename AI comp
if (AIFileFound) {
    AIComp.name = blenderComp.name + "_2D";
}

// Create folder for renders
var passesFolder = app.project.items.addFolder("BLENDER_RENDER");

// --- Find and import pass image sequences

// Get latest version of passes dir
var passesDir = getPassesDir(sq, sh);
passesDir = getLatestVersion(passesDir);
passesDir.changePath("sq{sq}_sh{sh}_passes".replace(/{sq}/g, sq).replace(/{sh}/g, sh));
var sequenceDirs = passesDir.getFiles();

print("PASSES:");
print(sequenceDirs);

// Import each image sequence
for (var i = sequenceDirs.length - 1; i >= 0; i--) {
    if (sequenceDirs[i].name.match(/_placeholder/)) {
        continue;
        }
    var files = sequenceDirs[i].getFiles();
    var sequenceStartFile = testForSequence(files);

    var importOptions = new ImportOptions(sequenceStartFile);
    importOptions.sequence = true;

    var importedFile = importSafeWithError(importOptions);

    importedFile.parentFolder = passesFolder;
    importedFile.mainSource.conformFrameRate = 24;

    var layer = blenderComp.layers.add(importedFile);

    if (layer.name.endsWith("000_ref") || layer.name.startsWith("000_")) {
        importedFile.label = 14;
        layer.label = 14;
        layer.guideLayer = true;
    }
}

// Sort layers based on supplied list from Blender
print("SORTING LAYERS");

// layersList should be provided by Libreflow.
// If not, try to find it near the original JSX.
if (typeof layersList == 'undefined') {
    var layerListPath = setupScriptPath.replace(/\.jsx/, "_layers.list");
    var layerListFile = new File(layerListPath);
    if (layerListFile.exists) {
        layerListFile.open("r");
        var layerList = layerListFile.read();
        layerListFile.close();
        layersList = layerList.split(/\n/);
    }
}
if (typeof layersList == 'undefined') {
    print("Could not find list of layers for sorting!");
}
else {
    var previousLayer = null;
    for (var i = 0; i < layersList.length; i++) {
        var layerNameFromList = layersList[i];
        print("LAYER:");
        print(layerNameFromList);

        // Get layer based on this name
        for (var j = 1; j <= blenderComp.layers.length; j++){
            var layer = blenderComp.layers[j];
            var layerNameActual = layer.name;

            if (layerNameActual.indexOf(layerNameFromList) != -1) {
                if (previousLayer == null) {
                    layer.moveToBeginning();
                }
                else {
                    layer.moveAfter(previousLayer);
                }
                previousLayer = layer;
            }
        }
    }
    delete layersList;
}

// TODO Find and import animation movie

// Setup main comps color
blenderComp.bgColor = bgColor;
if (AIFileFound) {
    AIComp.bgColor = bgColor;
}

for (var i = 1; i <= blenderComp.layers.length; i++) {
    layer = blenderComp.layers[i];
    // Set 000_ref as guided layer
    if (layer.name.endsWith("000_ref")) {
        layer.guideLayer = true;
    }
    // Hide first 4 layers
    if (layer.name.match(/0?[1-4]0_(?:mask|perspective|frame|storyboard)/)) {
        layer.enabled = false;
    }
    // Hide matte layers
    if (layer.name.match(/_Matte\.\[[-0-9]+\]\.png/)) {
        layer.enabled = false;
    }
}

app.endUndoGroup();
