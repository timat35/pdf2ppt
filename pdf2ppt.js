
// ============================================================================

const fs = require('fs');
var sizeOf = require('image-size');
var im = require('imagemagick');
var gConsoleLog = true;


// ============================================================================


// STEP 1: Load pptxgenjs and show version to verify everything loaded correctly
var PptxGenJS;
if (fs.existsSync('../dist/pptxgen.js')) {
	// for LOCAL TESTING
	PptxGenJS = require('../dist/pptxgen.js');
	if (gConsoleLog) console.log('-=TEST MODE=- (../dist/pptxgen.js)');
}
else {
	PptxGenJS = require("pptxgenjs");
}
var pptx = new PptxGenJS();

if (gConsoleLog) console.log(` * save location: ${__dirname}`);

// ============================================================================

// EX: Regular callback - will be sent the export filename once the file has been written to fs
function saveCallback(filename) {
	if (gConsoleLog) console.log('saveCallback: Good News Everyone! File created: '+ filename);
}

// EX: JSZip callback - take the specified output (`data`) and do whatever
function jszipCallback(data) {
	if (gConsoleLog) {
		console.log('jszipCallback: First 100 chars of output:\n');
		console.log( data.substring(0,100) );
	}
}

function getFiles(dir) {

    // get all 'files' in this directory
    var all = fs.readdirSync(dir);

    // process each checking directories and saving files
    return all.map(file => {
        // am I a directory?
        if (fs.statSync(`${dir}/${file}`).isDirectory()) {
            // recursively scan me for my files
            return getFiles(`${dir}/${file}`);
        }
        // WARNING! I could be something else here!!!
        return `${dir}/${file}`;     // file name (see warning)
    });
}


function addpptx (pdf_file) {
	

	return new Promise(function(resolve, reject) {
		

		im.convert(['-density', '300', pdf_file, '-resize', '100%',   '-compress','lzw', '-background','white', '-alpha','remove',pdf_file.replace(/pdf/g, "png")], 
		function(){
			console.log(pdf_file)
			dimensions = sizeOf(pdf_file.replace(/pdf/g, "png"));
			ratio = dimensions.width/dimensions.height;
			var slide = pptx.addNewSlide();	

			pptx_width = 10;
			pptx_heigth = pptx_width/ratio;
			pptx_x = 0;
			pptx_y = (7.5 - pptx_heigth) / 2;

			if (pptx_heigth > 6.5) {
				
			  pptx_heigth = 6.5;
			  pptx_width = pptx_heigth*ratio;
			  pptx_y = 0.5;
			  pptx_x = (10 - pptx_width) / 2;
				
			}

			slide.addImage({ path:pdf_file.replace(/pdf/g, "png"), x:pptx_x, y:pptx_y, w:pptx_width, h:pptx_heigth });
			resolve()
		
		});
		
	
	})
}


// ============================================================================


// STEP 3: Export another demo file
// HOWTO: Create a new Presenation
var pptx = new PptxGenJS();
if (gConsoleLog && process.argv.length != 3) console.log(` * pptxgenjs ver: ${pptx.version}`); // Loaded okay?

pptx.setLayout('LAYOUT_4x3');


var filetest = getFiles('./pdf')
var png_file = './temp/temp';
var ratio;
var dimensions;
var exportName = 'pdf2pptx';
var i = 1 
var finish = 0; 
	
//processPDF(filetest, exportName)

const promises = filetest.map(addpptx);

Promise.all(
	promises
).then(function() {
	pptx.save( exportName ); if (gConsoleLog) console.log('\nFile created:\n'+' * '+exportName);
	if (gConsoleLog) console.log(`
	-----------
	Job's done!
	-----------
	`);
});



