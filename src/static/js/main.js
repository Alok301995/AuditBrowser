// Description: Main JavaScript file for the attribute collection

// ***************  BEGINNING OF UTILITY CODE  ***************

function x64Add(m, n) {
  m = [m[0] >>> 16, m[0] & 0xffff, m[1] >>> 16, m[1] & 0xffff];
  n = [n[0] >>> 16, n[0] & 0xffff, n[1] >>> 16, n[1] & 0xffff];
  var o = [0, 0, 0, 0];
  o[3] += m[3] + n[3];
  o[2] += o[3] >>> 16;
  o[3] &= 0xffff;
  o[2] += m[2] + n[2];
  o[1] += o[2] >>> 16;
  o[2] &= 0xffff;
  o[1] += m[1] + n[1];
  o[0] += o[1] >>> 16;
  o[1] &= 0xffff;
  o[0] += m[0] + n[0];
  o[0] &= 0xffff;
  return [(o[0] << 16) | o[1], (o[2] << 16) | o[3]];
}

function x64Multiply(m, n) {
  m = [m[0] >>> 16, m[0] & 0xffff, m[1] >>> 16, m[1] & 0xffff];
  n = [n[0] >>> 16, n[0] & 0xffff, n[1] >>> 16, n[1] & 0xffff];
  var o = [0, 0, 0, 0];
  o[3] += m[3] * n[3];
  o[2] += o[3] >>> 16;
  o[3] &= 0xffff;
  o[2] += m[2] * n[3];
  o[1] += o[2] >>> 16;
  o[2] &= 0xffff;
  o[2] += m[3] * n[2];
  o[1] += o[2] >>> 16;
  o[2] &= 0xffff;
  o[1] += m[1] * n[3];
  o[0] += o[1] >>> 16;
  o[1] &= 0xffff;
  o[1] += m[2] * n[2];
  o[0] += o[1] >>> 16;
  o[1] &= 0xffff;
  o[1] += m[3] * n[1];
  o[0] += o[1] >>> 16;
  o[1] &= 0xffff;
  o[0] += m[0] * n[3] + m[1] * n[2] + m[2] * n[1] + m[3] * n[0];
  o[0] &= 0xffff;
  return [(o[0] << 16) | o[1], (o[2] << 16) | o[3]];
}

// Given a 64bit int (as an array of two 32bit ints) and an int
// representing a number of bit positions, returns the 64bit int (as an
// array of two 32bit ints) rotated left by that number of positions.

function x64Rotl(m, n) {
  n %= 64;
  if (n === 32) {
    return [m[1], m[0]];
  } else if (n < 32) {
    return [
      (m[0] << n) | (m[1] >>> (32 - n)),
      (m[1] << n) | (m[0] >>> (32 - n)),
    ];
  } else {
    n -= 32;
    return [
      (m[1] << n) | (m[0] >>> (32 - n)),
      (m[0] << n) | (m[1] >>> (32 - n)),
    ];
  }
}

// Given a 64bit int (as an array of two 32bit ints) and an int
// representing a number of bit positions, returns the 64bit int (as an
// array of two 32bit ints) shifted left by that number of positions.

function x64LeftShift(m, n) {
  n %= 64;
  if (n === 0) {
    return m;
  } else if (n < 32) {
    return [(m[0] << n) | (m[1] >>> (32 - n)), m[1] << n];
  } else {
    return [m[1] << (n - 32), 0];
  }
}

// Given two 64bit ints (as an array of two 32bit ints) returns the two
// xored together as a 64bit int (as an array of two 32bit ints).

function x64Xor(m, n) {
  return [m[0] ^ n[0], m[1] ^ n[1]];
}

// Given a block, returns murmurHash3's final x64 mix of that block.
// (`[0, h[0] >>> 1]` is a 33 bit unsigned right shift. This is the
// only place where we need to right shift 64bit ints.)

function x64Fmix(h) {
  h = x64Xor(h, [0, h[0] >>> 1]);
  h = x64Multiply(h, [0xff51afd7, 0xed558ccd]);
  h = x64Xor(h, [0, h[0] >>> 1]);
  h = x64Multiply(h, [0xc4ceb9fe, 0x1a85ec53]);
  h = x64Xor(h, [0, h[0] >>> 1]);
  return h;
}

// Given a string and an optional seed as an int, returns a 128 bit
// hash using the x64 flavor of MurmurHash3, as an unsigned hex.

function x64hash128(key, seed) {
  key = key || "";
  seed = seed || 0;
  var remainder = key.length % 16;
  var bytes = key.length - remainder;
  var h1 = [0, seed];
  var h2 = [0, seed];
  var k1 = [0, 0];
  var k2 = [0, 0];
  var c1 = [0x87c37b91, 0x114253d5];
  var c2 = [0x4cf5ad43, 0x2745937f];
  for (var i = 0; i < bytes; i = i + 16) {
    k1 = [
      (key.charCodeAt(i + 4) & 0xff) |
        ((key.charCodeAt(i + 5) & 0xff) << 8) |
        ((key.charCodeAt(i + 6) & 0xff) << 16) |
        ((key.charCodeAt(i + 7) & 0xff) << 24),
      (key.charCodeAt(i) & 0xff) |
        ((key.charCodeAt(i + 1) & 0xff) << 8) |
        ((key.charCodeAt(i + 2) & 0xff) << 16) |
        ((key.charCodeAt(i + 3) & 0xff) << 24),
    ];
    k2 = [
      (key.charCodeAt(i + 12) & 0xff) |
        ((key.charCodeAt(i + 13) & 0xff) << 8) |
        ((key.charCodeAt(i + 14) & 0xff) << 16) |
        ((key.charCodeAt(i + 15) & 0xff) << 24),
      (key.charCodeAt(i + 8) & 0xff) |
        ((key.charCodeAt(i + 9) & 0xff) << 8) |
        ((key.charCodeAt(i + 10) & 0xff) << 16) |
        ((key.charCodeAt(i + 11) & 0xff) << 24),
    ];
    k1 = x64Multiply(k1, c1);
    k1 = x64Rotl(k1, 31);
    k1 = x64Multiply(k1, c2);
    h1 = x64Xor(h1, k1);
    h1 = x64Rotl(h1, 27);
    h1 = x64Add(h1, h2);
    h1 = x64Add(x64Multiply(h1, [0, 5]), [0, 0x52dce729]);
    k2 = x64Multiply(k2, c2);
    k2 = x64Rotl(k2, 33);
    k2 = x64Multiply(k2, c1);
    h2 = x64Xor(h2, k2);
    h2 = x64Rotl(h2, 31);
    h2 = x64Add(h2, h1);
    h2 = x64Add(x64Multiply(h2, [0, 5]), [0, 0x38495ab5]);
  }
  k1 = [0, 0];
  k2 = [0, 0];
  switch (remainder) {
    case 15:
      k2 = x64Xor(k2, x64LeftShift([0, key.charCodeAt(i + 14)], 48));
    case 14:
      k2 = x64Xor(k2, x64LeftShift([0, key.charCodeAt(i + 13)], 40));
    case 13:
      k2 = x64Xor(k2, x64LeftShift([0, key.charCodeAt(i + 12)], 32));
    case 12:
      k2 = x64Xor(k2, x64LeftShift([0, key.charCodeAt(i + 11)], 24));
    case 11:
      k2 = x64Xor(k2, x64LeftShift([0, key.charCodeAt(i + 10)], 16));
    case 10:
      k2 = x64Xor(k2, x64LeftShift([0, key.charCodeAt(i + 9)], 8));
    case 9:
      k2 = x64Xor(k2, [0, key.charCodeAt(i + 8)]);
      k2 = x64Multiply(k2, c2);
      k2 = x64Rotl(k2, 33);
      k2 = x64Multiply(k2, c1);
      h2 = x64Xor(h2, k2);
    case 8:
      k1 = x64Xor(k1, x64LeftShift([0, key.charCodeAt(i + 7)], 56));
    case 7:
      k1 = x64Xor(k1, x64LeftShift([0, key.charCodeAt(i + 6)], 48));
    case 6:
      k1 = x64Xor(k1, x64LeftShift([0, key.charCodeAt(i + 5)], 40));
    case 5:
      k1 = x64Xor(k1, x64LeftShift([0, key.charCodeAt(i + 4)], 32));
    case 4:
      k1 = x64Xor(k1, x64LeftShift([0, key.charCodeAt(i + 3)], 24));
    case 3:
      k1 = x64Xor(k1, x64LeftShift([0, key.charCodeAt(i + 2)], 16));
    case 2:
      k1 = x64Xor(k1, x64LeftShift([0, key.charCodeAt(i + 1)], 8));
    case 1:
      k1 = x64Xor(k1, [0, key.charCodeAt(i)]);
      k1 = x64Multiply(k1, c1);
      k1 = x64Rotl(k1, 31);
      k1 = x64Multiply(k1, c2);
      h1 = x64Xor(h1, k1);
  }
  h1 = x64Xor(h1, [0, key.length]);
  h2 = x64Xor(h2, [0, key.length]);
  h1 = x64Add(h1, h2);
  h2 = x64Add(h2, h1);
  h1 = x64Fmix(h1);
  h2 = x64Fmix(h2);
  h1 = x64Add(h1, h2);
  h2 = x64Add(h2, h1);
  return (
    ("00000000" + (h1[0] >>> 0).toString(16)).slice(-8) +
    ("00000000" + (h1[1] >>> 0).toString(16)).slice(-8) +
    ("00000000" + (h2[0] >>> 0).toString(16)).slice(-8) +
    ("00000000" + (h2[1] >>> 0).toString(16)).slice(-8)
  );
}

const determine_randomized = function (
  run_1,
  run_2,
  catch_string,
  randomized_result
) {
  try {
    const run_1_result = run_1();
    const run_2_result = run_2();
    if (run_1_result == run_2_result) {
      return run_1_result;
    } else {
      return randomized_result || "randomized";
    }
  } catch (ex) {
    return catch_string || "undetermined";
  }
};

// ***************  GLOBAL OBJECT  ***************
var attributes = new Object();

// ***********************************************

// ***************  BEGINNING OF PLUGIN DETECT CODE  ***************
function identify_plugins() {
  // fetch and serialize plugins
  var plugins = "";
  if (navigator.plugins) {
    var np = navigator.plugins;
    var plist = new Array();
    for (var i = 0; i < np.length; i++) {
      plist[i] = np[i].name + "; ";
      plist[i] += np[i].description + "; ";
      plist[i] += np[i].filename + ";";
      for (var n = 0; n < np[i].length; n++) {
        plist[i] +=
          " (" +
          np[i][n].description +
          "; " +
          np[i][n].type +
          "; " +
          np[i][n].suffixes +
          ")";
      }
      plist[i] += ". ";
    }
    plist.sort();
    for (i = 0; i < np.length; i++) plugins += "Plugin " + i + ": " + plist[i];
  }
  // in IE, things are much harder; we use PluginDetect to get less
  // information (only the plugins listed below & their version numbers)
  if (plugins == "") {
    var pp = new Array();
    pp[0] = "Java";
    pp[1] = "QuickTime";
    pp[2] = "DevalVR";
    pp[3] = "Shockwave";
    pp[4] = "Flash";
    pp[5] = "WindowsMediaplayer";
    pp[6] = "Silverlight";
    pp[7] = "VLC";
    var version;
    for (p in pp) {
      version = PluginDetect.getVersion(pp[p]);
      if (version) plugins += pp[p] + " " + version + "; ";
    }
    plugins += ieAcrobatVersion();
  }
  return plugins;
}

// ***************  BEGINNING OF ACROBAT VERSION CODE  ***************
function ieAcrobatVersion() {
  // estimate the version of Acrobat on IE using horrible horrible hacks
  if (window.ActiveXObject) {
    for (var x = 2; x < 10; x++) {
      try {
        oAcro = eval("new ActiveXObject('PDF.PdfCtrl." + x + "');");
        if (oAcro) return "Adobe Acrobat version" + x + ".?";
      } catch (ex) {}
    }
    try {
      oAcro4 = new ActiveXObject("PDF.PdfCtrl.1");
      if (oAcro4) return "Adobe Acrobat version 4.?";
    } catch (ex) {}
    try {
      oAcro7 = new ActiveXObject("AcroPDF.PDF.1");
      if (oAcro7) return "Adobe Acrobat version 7.?";
    } catch (ex) {}
    return "";
  }
}

// ***************  BEGINNING OF DOM STORAGE CODE  ***************

function set_dom_storage() {
  try {
    localStorage.panopticlick = "yea";
    sessionStorage.panopticlick = "yea";
  } catch (ex) {}
}

function test_dom_storage() {
  var supported = "";
  try {
    if (localStorage.panopticlick == "yea") {
      supported += "DOM localStorage: Yes";
    } else {
      supported += "DOM localStorage: No";
    }
  } catch (ex) {
    supported += "DOM localStorage: No";
  }

  try {
    if (sessionStorage.panopticlick == "yea") {
      supported += ", DOM sessionStorage: Yes";
    } else {
      supported += ", DOM sessionStorage: No";
    }
  } catch (ex) {
    supported += ", DOM sessionStorage: No";
  }

  return supported;
}

function test_ie_userdata() {
  try {
    oPersistDiv.setAttribute("remember", "remember this value");
    oPersistDiv.save("oXMLStore");
    oPersistDiv.setAttribute("remember", "overwritten!");
    oPersistDiv.load("oXMLStore");
    if ("remember this value" == oPersistDiv.getAttribute("remember")) {
      return ", IE userData: Yes";
    } else {
      return ", IE userData: No";
    }
  } catch (ex) {
    return ", IE userData: No";
  }
}

function test_open_database() {
  return ", openDatabase: " + !!window.openDatabase;
}

function test_indexed_db() {
  try {
    return ", indexed db: " + !!window.indexedDB;
  } catch (e) {
    return ", indexed db: true";
  }
}


// ***************  BEGINNING OF TOUCH SUPPORT CODE  ***************

function get_touch_support(touch_support) {
  var touch_support_str = "";
  touch_support_str += "Max touchpoints: " + String(touch_support[0]);
  touch_support_str += "; TouchEvent supported: " + String(touch_support[1]);
  touch_support_str += "; onTouchStart supported: " + String(touch_support[2]);
  return touch_support_str;
}

// ***************  BEGINNING OF FONT DETECTION CODE  ***************
function detectFonts() {
  // Create a hidden div element
  const testDiv = document.createElement("div");
  testDiv.style.position = "absolute";
  testDiv.style.top = "-9999px";
  testDiv.style.left = "-9999px";
  testDiv.style.visibility = "hidden";
  testDiv.innerHTML =
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";

  // Append the div to the document
  document.body.appendChild(testDiv);

  // Get the computed font styles
  const styles = window.getComputedStyle(testDiv);
  const fontFamilies = styles.getPropertyValue("font-family");

  // Remove the test div from the document
  document.body.removeChild(testDiv);

  // Split the font families into an array
  const fonts = fontFamilies.split(",");

  // Remove any quotes around the font names
  // const cleanFonts = fonts.map(font => font.replace(/['"]+/g, ''));

  // return cleanFonts;
  return fonts;
}

// ***************  BEGINNING OF CANVAS DETECTION CODE  ***************

function generateCanvasHash() {
  // Create a canvas element
  const canvas = document.createElement("canvas");
  const ctx = canvas.getContext("2d");

  // Set canvas dimensions
  canvas.width = 200;
  canvas.height = 50;

  // Set some text and styles for drawing on the canvas
  const text = "Hello, World!";
  ctx.font = "20px Arial";
  ctx.fillStyle = "#000000";
  ctx.fillText(text, 10, 30);

  // Generate hash from canvas data
  const data = canvas.toDataURL();
  const hash = data;

  // Return hash value
  return hash;
}

// ***************  BEGINNING OF WEBGL DETECTION CODE  ***************

function generateWebGLHash() {
  // Get WebGL context
  const canvas = document.createElement("canvas");
  const gl =
    canvas.getContext("webgl") || canvas.getContext("experimental-webgl");

  // Check if WebGL is supported
  if (!gl) {
    return null;
  }

  // Get WebGL parameters
  const renderer = gl.getParameter(gl.RENDERER);
  const vendor = gl.getParameter(gl.VENDOR);
  const version = gl.getParameter(gl.VERSION);
  const shadingLanguageVersion = gl.getParameter(gl.SHADING_LANGUAGE_VERSION);

  // Concatenate WebGL parameters to form hash
  const hash = `${renderer}~${vendor}~${version}~${shadingLanguageVersion}`;
  const webgl_vendor_renderer = `${vendor}~${renderer}`;
  // Return hash value
  return [hash, webgl_vendor_renderer];
}

// ***************  BEGINNING OF TOUCH DETECTION CODE  ***************

function getTouchSupport() {
  var maxTouchPoints = 0;
  var touchEvent = false;
  if (typeof navigator.maxTouchPoints !== "undefined") {
    maxTouchPoints = navigator.maxTouchPoints;
  } else if (typeof navigator.msMaxTouchPoints !== "undefined") {
    maxTouchPoints = navigator.msMaxTouchPoints;
  }
  try {
    document.createEvent("TouchEvent");
    touchEvent = true;
  } catch (_) {
    /* squelch */
  }
  var touchStart = "ontouchstart" in window;
  return `Max Touch Points: ${maxTouchPoints}, Touch Event: ${touchEvent}, Touch Start: ${touchStart}`;
}

// ***************  BEGINNING OF TIMEZONE DETECTION CODE  ***************

function getTimezoneString() {
  const date = new Date();
  const timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
  const timezoneOffset = date
    .toLocaleString("en-US", { timeZone: timezone, timeZoneName: "short" })
    .split(" ")[2];

  return `${timezone} (${timezoneOffset})`;
}

// ***************  BEGINNING OF AD BLOCK DETECTION CODE  ***************

function isAdblockUsed() {
  const d = document;

  if (!d.body?.appendChild) {
    return false;
  }

  const ads = d.createElement("div");
  ads.innerHTML = "&nbsp;";
  ads.className = "adsbox";

  try {
    d.body.appendChild(ads);
    const node = d.querySelector(".adsbox");
    return !node || node.offsetHeight === 0;
  } finally {
    ads.parentNode?.removeChild(ads);
  }
}



// ***************  BEGINNING OF FONT DETECTION CODE  ***************


const testString = "mmMwWLliI0O&1";
const testSize = "48px";
const baseFonts = ["monospace", "sans-serif", "serif"];
const fontList = [
  "sans-serif-thin",
  "ARNO PRO",
  "Agency FB",
  "Arabic Typesetting",
  "Arial Unicode MS",
  "AvantGarde Bk BT",
  "BankGothic Md BT",
  "Batang",
  "Bitstream Vera Sans Mono",
  "Calibri",
  "Century",
  "Century Gothic",
  "Clarendon",
  "EUROSTILE",
  "Franklin Gothic",
  "Futura Bk BT",
  "Futura Md BT",
  "GOTHAM",
  "Gill Sans",
  "HELV",
  "Haettenschweiler",
  "Helvetica Neue",
  "Humanst521 BT",
  "Leelawadee",
  "Letter Gothic",
  "Levenim MT",
  "Lucida Bright",
  "Lucida Sans",
  "Menlo",
  "MS Mincho",
  "MS Outlook",
  "MS Reference Specialty",
  "MS UI Gothic",
  "MT Extra",
  "MYRIAD PRO",
  "Marlett",
  "Meiryo UI",
  "Microsoft Uighur",
  "Minion Pro",
  "Monotype Corsiva",
  "PMingLiU",
  "Pristina",
  "SCRIPTINA",
  "Segoe UI Light",
  "Serifa",
  "SimHei",
  "Small Fonts",
  "Staccato222 BT",
  "TRAJAN PRO",
  "Univers CE 55 Medium",
  "Vrinda",
  "ZWAdobeF",
];

const fontSpanStyle = {
  // CSS font reset to reset external styles
  fontStyle: "normal",
  fontWeight: "normal",
  letterSpacing: "normal",
  lineBreak: "auto",
  lineHeight: "normal",
  textTransform: "none",
  textAlign: "left",
  textDecoration: "none",
  textShadow: "none",
  whiteSpace: "normal",
  wordBreak: "normal",
  wordSpacing: "normal",
  position: "absolute",
  left: "-9999px",
  fontSize: testSize,
};

function getFonts() {
  const d = document;
  const holder = d.body;

  // div to load spans for the base fonts
  const baseFontsDiv = d.createElement("div");

  // div to load spans for the fonts to detect
  const fontsDiv = d.createElement("div");

  const defaultWidth = {};
  const defaultHeight = {};

  // creates a span where the fonts will be loaded
  const createSpan = () => {
    const span = d.createElement("span");
    span.textContent = testString;

    for (const prop of Object.keys(fontSpanStyle)) {
      span.style[prop] = fontSpanStyle[prop];
    }

    return span;
  };

  // creates a span and load the font to detect and a base font for fallback
  const createSpanWithFonts = (fontToDetect, baseFont) => {
    const s = createSpan();
    s.style.fontFamily = `'${fontToDetect}',${baseFont}`;
    return s;
  };

  // creates spans for the base fonts and adds them to baseFontsDiv
  const initializeBaseFontsSpans = () => {
    return baseFonts.map((baseFont) => {
      const s = createSpan();
      s.style.fontFamily = baseFont;
      baseFontsDiv.appendChild(s);
      return s;
    });
  };

  // creates spans for the fonts to detect and adds them to fontsDiv
  const initializeFontsSpans = () => {
    // Stores {fontName : [spans for that font]}
    const spans = {};

    for (const font of fontList) {
      spans[font] = baseFonts.map((baseFont) => {
        const s = createSpanWithFonts(font, baseFont);
        fontsDiv.appendChild(s);
        return s;
      });
    }

    return spans;
  };

  // checks if a font is available
  const isFontAvailable = (fontSpans) => {
    return baseFonts.some(
      (baseFont, baseFontIndex) =>
        fontSpans[baseFontIndex].offsetWidth !== defaultWidth[baseFont] ||
        fontSpans[baseFontIndex].offsetHeight !== defaultHeight[baseFont]
    );
  };

  // create spans for base fonts
  const baseFontsSpans = initializeBaseFontsSpans();

  // add the spans to the DOM
  holder.appendChild(baseFontsDiv);

  // get the default width for the three base fonts
  for (let index = 0, length = baseFonts.length; index < length; index++) {
    defaultWidth[baseFonts[index]] = baseFontsSpans[index].offsetWidth; // width for the default font
    defaultHeight[baseFonts[index]] = baseFontsSpans[index].offsetHeight; // height for the default font
  }

  // create spans for fonts to detect
  const fontsSpans = initializeFontsSpans();

  // add all the spans to the DOM
  holder.appendChild(fontsDiv);

  // check available fonts
  const available = [];
  for (let i = 0, l = fontList.length; i < l; i++) {
    if (isFontAvailable(fontsSpans[fontList[i]])) {
      available.push(fontList[i]);
    }
  }

  // remove spans from DOM
  holder.removeChild(fontsDiv);
  holder.removeChild(baseFontsDiv);
  return available;
}



// ********** START OF AUDIO FP ********** //

var audioFingerprint = (function () {
  var context = null;
  var currentTime = null;
  var oscillator = null;
  var compressor = null;
  var fingerprint = null;
  var callback = null;

  function run(cb, debug = false) {
    callback = cb;

    try {
      setup();

      oscillator.connect(compressor);
      compressor.connect(context.destination);

      oscillator.start(0);
      context.startRendering();

      context.oncomplete = onComplete;
    } catch (e) {
      if (debug) {
        throw e;
      }
    }
  }

  function setup() {
    setContext();
    currentTime = context.currentTime;
    setOscillator();
    setCompressor();
  }

  function setContext() {
    var audioContext =
      window.OfflineAudioContext || window.webkitOfflineAudioContext;
    context = new audioContext(1, 44100, 44100);
  }

  function setOscillator() {
    oscillator = context.createOscillator();
    oscillator.type = "triangle";
    oscillator.frequency.setValueAtTime(10000, currentTime);
  }

  function setCompressor() {
    compressor = context.createDynamicsCompressor();

    setCompressorValueIfDefined("threshold", -50);
    setCompressorValueIfDefined("knee", 40);
    setCompressorValueIfDefined("ratio", 12);
    setCompressorValueIfDefined("reduction", -20);
    setCompressorValueIfDefined("attack", 0);
    setCompressorValueIfDefined("release", 0.25);
  }

  function setCompressorValueIfDefined(item, value) {
    if (
      compressor[item] !== undefined &&
      typeof compressor[item].setValueAtTime === "function"
    ) {
      compressor[item].setValueAtTime(value, context.currentTime);
    }
  }

  function onComplete(event) {
    generateFingerprints(event);
    compressor.disconnect();
  }

  function generateFingerprints(event) {
    var output = null;
    for (var i = 4500; 5e3 > i; i++) {
      var channelData = event.renderedBuffer.getChannelData(0)[i];
      output += Math.abs(channelData);
    }

    fingerprint = output.toString();

    if (typeof callback === "function") {
      return callback(fingerprint);
    }
  }

  return {
    run: run,
  };
})();

set_dom_storage();


// ********** END OF FUNCTIONS ********** //

// ********** START OF STORING WHORLS ********** //

try {
  attributes["video"] =
    screen.width + "x" + screen.height + "x" + screen.colorDepth;
} catch (ex) {
  attributes["video"] = "permission denied";
}

attributes["language"] = navigator.language;

attributes["platform"] = navigator.platform;

attributes["cpu_class"] = navigator.cpuClass || "N/A";

attributes["hardware_concurrency"] = navigator.hardwareConcurrency || "N/A";

attributes["device_memory"] = navigator.deviceMemory || "N/A";

attributes["supercookies_v2"] = determine_randomized(
  () =>
    test_dom_storage() +
    test_ie_userdata() +
    test_open_database() +
    test_indexed_db(),
  () =>
    test_dom_storage() +
    test_ie_userdata() +
    test_open_database() +
    test_indexed_db()
);

attributes["timezone"] = determine_randomized(
  () => new Date().getTimezoneOffset(),
  () => new Date().getTimezoneOffset(),
  "permission_denied"
);

attributes["plugins"] = determine_randomized(
  () => identify_plugins(),
  () => identify_plugins(),
  "permission denied"
);

attributes["canvas_hash"] = x64hash128(generateCanvasHash(), 31);

attributes["webgl_hash"] = x64hash128(generateWebGLHash()[0], 31);

attributes["loads_remote_fonts"] = document.fonts.check("bold 12px WorkSans");

let ios_lockdown = false;
if (
  !attributes["loads_remote_fonts"] &&
  /^Mozilla.+iPhone OS 16_/.test(navigator.userAgent)
) {
  ios_lockdown = true;
}

attributes["webgl_vendor_renderer"] = generateWebGLHash()[1];

attributes["timezone"] = getTimezoneString();

attributes["adblock"] = isAdblockUsed();

attributes["fonts"] = getFonts().toString();

audioFingerprint.run(function (fingerprint) {
  attributes["audio"] = fingerprint;
});
attributes["touch_support"] = getTouchSupport();

// ********** END OF WHORLS ********** //

export function get_attributes(){
  return attributes;
}
