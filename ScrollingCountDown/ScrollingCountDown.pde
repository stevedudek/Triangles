//
// "Triangulates" a jpeg image
//
// How to use:
//
// Put a jpeg (or jpg) image of your choice in the directory with this sketch
// Point the sketch to your image by setting below 'String filename = "your_image.jpg";'
//
// Changing the vertcenter and horizcenter toggles will select either the center or top of the image
//
// hsv correction leads to some odd colored artifacts.
//
// This sketch...
//
// First, crops the image to fit the ratio of the hex array (1:1.15 depending on flat or pointy top)
// Then, averages the r,g,b values within each hex
//
// Version 4 converts each r,g,b to h,s,v; averages those; and re-converts the average h,s,v back to r,g,b
// Version 5 corrects for rhombal coordinates. It also includes a toggle for hsv correction.
// Version 6 is written in proper Java OOP format
// Version 7 dumps the rgb coordinate output to a text file
//

int numBigTri = 6;  // Number of Big Triangles

// Relative coordinates for the Big Triangles
int[][] BigTriCoord = {
  {0,0},  // Strip 1
  {0,1},  // Strip 2
  {2,0},  // Strip 3
  {2,1},  // Strip 4
  {1,0},  // Strip 5
  {1,1}   // Strip 6
};

// Matrix listing where the connector attaches physically
// to each Big Triangle.
// First value is Corner (Pixel 0) of connector attachment
// 'L' = Left, 'R' = Right, 'C' = Center
// Second value is Direction of lights (0->1) from connector
// as viewed from corner
// 'L' = Left, 'R' = Right
char[][] connectors = {
  {'L','R'},  // Strip 1
  {'L','R'},  // Strip 2
  {'L','R'},  // Strip 3
  {'L','R'},  // Strip 4
  {'L','R'},  // Strip 5
  {'L','R'}   // Strip 6
};

class TestObserver implements Observer {
  public boolean hasStrips = false;
  public void update(Observable registry, Object updatedDevice) {
    println("Registry changed!");
    if (updatedDevice != null) {
      println("Device change: " + updatedDevice);
    }
    this.hasStrips = true;
  }
}

TestObserver testObserver;

// Physical strip registry
DeviceRegistry registry;
List<Strip> strips = new ArrayList<Strip>();

int NONE = 9999;  // hack: "null" for "int'

//
// Controller on the bottom of the screen
//
// Draw labels has 3 states:
// 0:LED number, 1:(x,y) coordinate, and 2:none
int DRAW_LABELS = 2;

// Tiling!
// true means draw all the Big Triangles
// false means all Big Triangles overlap
boolean TILING = true;

int BRIGHTNESS = 100;  // A percentage
int COLOR_STATE = 0;  // no enum types in processing. Messy

// Count down globals
int number_counter = 30;  // Starting seconds
float begin_scroll = 0.0;
float end_scroll = 2.0;
boolean count_down = false;  // Don't change this
long savedTime;
String filename = "11.jpg";

boolean vertcenter = true;         // Do you want to take a vertical center slice of the image?
boolean horizcenter = false;        // Do you want to take a horizontal center slice of the image?
boolean printnumoutput = false;    // Do you want the r,g,b values printed out
boolean hsvcorrect = false;         // Do you want to hsv correct the colors?

// How many triangles on the base
int TRI_GEN = 12;
int ROW_WIDTH = TRI_GEN * 2;
int NUM_PIXELS = TRI_GEN * ROW_WIDTH;

// Color buffers: [BigTri][Pixel][r,g,b]
// Two buffers permits updating only the lights that change color
// May improve performance and reduce flickering
int[][][] curr_buffer = new int[numBigTri][NUM_PIXELS][3];
int[][][] next_buffer = new int[numBigTri][NUM_PIXELS][3];

// Calculated pixel constants for simulator display
int SCREEN_SIZE = 800;  // square screen
float TRI_SIZE = (SCREEN_SIZE - 20) / (TRI_GEN * grid_width());  // Scale triangles to fit screen
float TRI_HEIGHT = TRI_SIZE * 0.866;
float widthheight = 1 / 0.866;  // Width-to-heigh ratio for an equilateral triangle
int BASE = (int)(TRI_GEN * TRI_SIZE);  // Width of big triangle
int BIG_HEIGHT = (int)triHeight(BASE);  // Height of big triangle
int SCREEN_WIDTH = (int)(BASE * grid_width()) + 20;  // Width + a little
int SCREEN_HEIGHT = (BIG_HEIGHT * grid_height()) + 20; // Height + a little
int CORNER_X = 10; // bottom left corner position on the screen
int CORNER_Y = SCREEN_HEIGHT - 10; // bottom left corner position on the screen

// Grid model(s) of Big Triangles
TriForm[] triGrid = new TriForm[numBigTri];

// Brute-force arrays of triangle numbers
// used for rotations of the whole Triangle
int[] rotateclock = {
  22,21,23,24,62,61,63,64,94,93,95,96,118,117,119,120,134,133,135,136,142,141,143,
  140,138,137,131,132,122,121,115,116,98,97,91,92,66,65,59,60,26,25,19,20,
  18,17,27,28,58,57,67,68,90,89,99,100,114,113,123,124,130,129,139,
  128,126,125,111,112,102,101,87,88,70,69,55,56,30,29,15,16,
  14,13,31,32,54,53,71,72,86,85,103,104,110,109,127,
  108,106,105,83,84,74,73,51,52,34,33,11,12,
  10,9,35,36,50,49,75,76,82,81,107,
  80,78,77,47,48,38,37,7,8,
  6,5,39,40,46,45,79,
  44,42,41,3,4,
  2,1,43,
  0 };
  
int[] rotatecounter = {
  143,141,140,138,139,129,128,126,127,109,108,106,107,81,80,78,79,45,44,42,43,1,0,
  2,3,41,40,46,47,77,76,82,83,105,104,110,111,125,124,130,131,137,136,142,
  135,133,132,122,123,113,112,102,103,85,84,74,75,49,48,38,39,5,4,
  6,7,37,36,50,51,73,72,86,87,101,100,114,115,121,120,134,
  119,117,116,98,99,89,88,70,71,53,52,34,35,9,8,
  10,11,33,32,54,55,69,68,90,91,97,96,118,
  95,93,92,66,67,57,56,30,31,13,12,
  14,15,29,28,58,59,65,64,94,
  63,61,60,26,27,17,16,
  18,19,25,24,62,
  23,21,20,
  22 };

import com.heroicrobot.dropbit.registry.*;
import com.heroicrobot.dropbit.devices.pixelpusher.Pixel;
import com.heroicrobot.dropbit.devices.pixelpusher.Strip;
import com.heroicrobot.dropbit.devices.pixelpusher.PixelPusher;
import com.heroicrobot.dropbit.devices.pixelpusher.PusherCommand;

import processing.net.*;
import java.util.*;
import java.util.regex.*;


// Cropped part of the image
int startWidth, endWidth, imgWidth, startHeight, endHeight, imgHeight;  

PImage img;  // the number picture
PImage bgnd;  // the black background

class Coord {
  public int x, y;
  
  Coord(int x, int y) {
    this.x = x;
    this.y = y;
  }
  
  boolean outofbounds() {  // is coordinate off of the array?
    if (x < 0 || x >= TRI_GEN * 2 || y < 0 || y >= TRI_GEN) {
      return(true);  // Would be a dangerous access of memory. Crash!
    } else {
      return(false);
    }
  }
  
  boolean isOnTriangle() {  // is coordinate on the main triangle grid?
    if (y < 0 || y >= TRI_GEN || x < y || x >= (ROW_WIDTH - y -1)) {
      return false;
    } else {
      return true;
    }
  }
}

class RGBColor {
  public float r, g, b;
  
  RGBColor(float r, float g, float b) {
    this.r = r;
    this.g = g;
    this.b = b;
  }
}

class Pixel {
  public int numitems;
  public RGBColor pixcolor;
  
  Pixel() {
    this.numitems = 0;
  }
}

class PixelArray {
  public int size;
  public Pixel[] Pixels;
  
  PixelArray(int size) {
    this.size = size;
    this.Pixels = new Pixel[size];
    for (int i = 0; i < size; i++) {
      Pixels[i] = new Pixel();
    }
    BlackAllPixels();
  }
  
  void EmptyAllPixels() {
    for (int i = 0; i < size; i++) EmptyPixel(i);
  }
  
  void EmptyPixel(int index) {
    if (index < 0 || index >= size) {
       return;
    } else {
      Pixels[index].numitems = 0;
    }
  }
  
  void BlackAllPixels() {
    RGBColor black = new RGBColor(0,0,0);
    for (int i = 0; i < size; i++) StuffPixelWithColor(i, black);
  }
  
  void StuffPixelWithColor(int index, RGBColor rgb) {
    if (index < 0 || index >= size) return;
    
    int numdata = Pixels[index].numitems;
    if (numdata == 0) {  // First value in pixel. Stuff all of it.
      this.Pixels[index].pixcolor = new RGBColor(rgb.r, rgb.g, rgb.b);
    } else {  // Already values in hex. Do a weighted average with the new value.
      this.Pixels[index].pixcolor = new RGBColor(
        (rgb.r + (this.Pixels[index].pixcolor.r*numdata))/(numdata+1),
        (rgb.g + (this.Pixels[index].pixcolor.g*numdata))/(numdata+1),
        (rgb.b + (this.Pixels[index].pixcolor.b*numdata))/(numdata+1));
    }
    this.Pixels[index].numitems++;
  }
}

// The main hex structure
PixelArray pixelarray;

void setup() {
  size(SCREEN_WIDTH, SCREEN_HEIGHT + 50); // 50 for controls
  stroke(0);
  fill(255,255,0);
  
  frameRate(10); // default 60 seems excessive
  
  // Set up the Big Triangles and stuff in the little triangles
  for (int i = 0; i < numBigTri; i++) {
    if (TILING) {  // Each Big Triangle has its own positioning
      triGrid[i] = makeTriGrid(getBigX(i), getBigY(i), i);
    } else {  // Draw all Big Triangles on top of each other at (0,0)
      triGrid[i] = makeTriGrid(0,0,i);
    }
  }
  
  registry = new DeviceRegistry();
  testObserver = new TestObserver();
  registry.addObserver(testObserver);
  colorMode(RGB, 255);
  frameRate(60);
  prepareExitHandler();
  strips = registry.getStrips();  // Array of strips?
  
  initializeColorBuffers();  // Stuff with zeros (all black)
  
  //_server = new Server(this, port);
  //println("server listening:" + _server);
  
  // Image handling
  pixelarray = new PixelArray(NUM_PIXELS);
  
  forceBlack();
}

void draw() {
  background(200);
  
  drawBottomControls();
  
  // Draw each grid
  for (int i = 0; i < numBigTri; i++) {
    triGrid[i].draw();
  }
  // Draw a bold frame around each grid
  if (TILING) {
    for (int i = 0; i < numBigTri; i++) {
      drawBigFrame(i);
    }
  }
  
  if (count_down) {
    if (number_counter >= 0) {  // We're counting!
      long currTime = millis();
      long diffTime = currTime - savedTime;
      
      if (diffTime > 1000) {  // 1 second
        savedTime = currTime + 1000 - diffTime;
        diffTime -= 1000;
        number_counter -= 1;
        if (number_counter < 0) {
          count_down = false;
          forceBlack();
        }
        if (number_counter <= 11 && number_counter >= 0) {
          filename = number_counter + ".jpg";
        }
      }
      if (number_counter < 12 && count_down) {  // We're displaying!
        BlendImages(filename, calc_scroll_amount(diffTime));
        DumpImageIntoPixels();
        movePixelsToBuffer();
        sendDataToLights();
        pushColorBuffer();
        pixelarray.EmptyAllPixels();
      }
    }
  }
}

float calc_scroll_amount(long time) {
  if (time > 1000) time = 1000;
  return (begin_scroll + ((end_scroll - begin_scroll) * time / 1000));
}

void BlendImages(String file_name, float scroll_amount) {
  img = loadImage(file_name);  // Load number picture
  img.loadPixels();
  
  // Figure out the cropped dimensions of the image
  CalcPixelParameters(img.width, img.height);
  int numberHeight = endHeight - startHeight;
  int backWidth = (int)(numberHeight / 0.866);
  
  // Create the screen image and fill it with all black
  bgnd = createImage(backWidth, numberHeight, RGB);
  bgnd.loadPixels();
  
  for (int i = 0; i < bgnd.pixels.length; i++) {
    bgnd.pixels[i] = color(0, 0, 0);  // Black
  }
  // Now blend
  if (scroll_amount < 1.0) {  // Number is coming in from left of screen
    int crop_start = (int)((endWidth-startWidth)*(1.0 - scroll_amount));
    
    bgnd.blend(img,  // src
      startWidth + crop_start,  //sx
      startHeight,  // sy
      (endWidth - startWidth) - crop_start,  // sw
      numberHeight,  // sh
      0,  // dx
      0,  // dy
      (endWidth - startWidth) - crop_start,  // dw
      bgnd.height,  // dh
      LIGHTEST);
  } else {  // Number is leaving to right of screen
    int crop_start = (int)(bgnd.width * (scroll_amount - 1.0));
    bgnd.blend(img,  // src
      0,  //sx
      startHeight,  // sy
      bgnd.width - crop_start,  // sw
      numberHeight,  // sh
      crop_start,  // dx
      0,  // dy
      bgnd.width - crop_start,  // dw
      bgnd.height,  // dh
      LIGHTEST);
  }
  bgnd.updatePixels();
}

void DumpImageIntoPixels() {

  // Figure out the cropped dimensions of the image
  // Figure out the size of each little hex. Sets globals
  // CalcPixelParameters(bgnd.width, bgnd.height);
  
  // Iterate over the active size of the image pixel-by-pixel
  // For each pixel, determine the triangular coordinate
  for (int j = 0; j < bgnd.height; j++) {
    for (int i = 0; i < bgnd.width; i++) {
      Coord coord = GetPixelCoord(i, j, bgnd.height, bgnd.width);
      if (coord.outofbounds()) continue;
      
      // Pull pixel location and color from picture
      int imageloc = i + j*bgnd.width;
      RGBColor rgb = new RGBColor(red(bgnd.pixels[imageloc]),
                       green(bgnd.pixels[imageloc]),
                        blue(bgnd.pixels[imageloc]));
      
      // Stuff the pixel's rgb color data into the proper hex bin
      if (hsvcorrect) {   // Do we correct for hsv?
        RGBColor hsv = RGBtoHSV(rgb);  // Yes, rgb -> hsv
        pixelarray.StuffPixelWithColor(get_index(coord), hsv);
      } else {
        pixelarray.StuffPixelWithColor(get_index(coord), rgb);
      }      
    }
  }
}

void drawCheckbox(int x, int y, int size, color fill, boolean checked) {
  stroke(0);
  fill(fill);  
  rect(x,y,size,size);
  if (checked) {    
    line(x,y,x+size,y+size);
    line(x+size,y,x,y+size);
  }  
}

void drawBottomControls() {
  // draw a bottom white region
  fill(255,255,255);
  rect(0,SCREEN_HEIGHT,SCREEN_WIDTH,40);
  
  // draw divider lines
  stroke(0);
  line(140,SCREEN_HEIGHT,140,SCREEN_HEIGHT+40);
  line(290,SCREEN_HEIGHT,290,SCREEN_HEIGHT+40);
  line(470,SCREEN_HEIGHT,470,SCREEN_HEIGHT+40);
  
  // draw checkboxes
  stroke(0);
  fill(255);
  // Checkbox is always unchecked; it is 3-state
  drawCheckbox(20,SCREEN_HEIGHT+10,20, color(255,255,255), count_down);
  
  rect(200,SCREEN_HEIGHT+4,15,15);  // minus brightness
  rect(200,SCREEN_HEIGHT+22,15,15);  // plus brightness
  
  drawCheckbox(340,SCREEN_HEIGHT+4,15, color(255,0,0), COLOR_STATE == 1);
  drawCheckbox(340,SCREEN_HEIGHT+22,15, color(255,0,0), COLOR_STATE == 4);
  drawCheckbox(360,SCREEN_HEIGHT+4,15, color(0,255,0), COLOR_STATE == 2);
  drawCheckbox(360,SCREEN_HEIGHT+22,15, color(0,255,0), COLOR_STATE == 5);
  drawCheckbox(380,SCREEN_HEIGHT+4,15, color(0,0,255), COLOR_STATE == 3);
  drawCheckbox(380,SCREEN_HEIGHT+22,15, color(0,0,255), COLOR_STATE == 6);
  
  drawCheckbox(400,SCREEN_HEIGHT+10,20, color(255,255,255), COLOR_STATE == 0);
     
  // draw text labels in 12-point Helvetica
  fill(0);
  textAlign(LEFT);
  PFont f = createFont("Helvetica", 12, true);
  textFont(f, 12);  
  text("30 sec start", 50, SCREEN_HEIGHT+25);
  
  text("-", 190, SCREEN_HEIGHT+16);
  text("+", 190, SCREEN_HEIGHT+34);
  text("Seconds", 225, SCREEN_HEIGHT+25);
  textFont(f, 20);
  text(number_counter, 150, SCREEN_HEIGHT+28);
  
  textFont(f, 12);
  text("None", 305, SCREEN_HEIGHT+16);
  text("All", 318, SCREEN_HEIGHT+34);
  text("Color", 430, SCREEN_HEIGHT+25);
  
  // scale font to size of triangles
  int font_size = 12;  // default size
  if (TRI_GEN >= 10) font_size = 8;  // smaller for small triangles
  if (TRI_GEN <= 6) font_size = 12;  // bigger for fewer triangles
  f = createFont("Helvetica", font_size, true);
  textFont(f, font_size);
  
}

void mouseClicked() {  
  //println("click! x:" + mouseX + " y:" + mouseY);
  if (mouseX > 20 && mouseX < 40 && mouseY > SCREEN_HEIGHT+10 && mouseY < SCREEN_HEIGHT+30) {
    // clicked draw labels button
    count_down = !count_down;
    if (count_down) savedTime = millis();
   
  }  else if (mouseX > 200 && mouseX < 215 && mouseY > SCREEN_HEIGHT+4 && mouseY < SCREEN_HEIGHT+19) {
    // Bright down checkbox  
    if (BRIGHTNESS > 10) BRIGHTNESS -= 5;
   
    // Bright up checkbox
  } else if (mouseX > 200 && mouseX < 215 && mouseY > SCREEN_HEIGHT+22 && mouseY < SCREEN_HEIGHT+37) {
      if (BRIGHTNESS <= 95) BRIGHTNESS += 5;
  
  }  else if (mouseX > 400 && mouseX < 420 && mouseY > SCREEN_HEIGHT+10 && mouseY < SCREEN_HEIGHT+30) {
    // No color correction  
    COLOR_STATE = 0;
   
  }  else if (mouseX > 340 && mouseX < 355 && mouseY > SCREEN_HEIGHT+4 && mouseY < SCREEN_HEIGHT+19) {
    // None red  
    COLOR_STATE = 1;
   
  }  else if (mouseX > 340 && mouseX < 355 && mouseY > SCREEN_HEIGHT+22 && mouseY < SCREEN_HEIGHT+37) {
    // All red  
    COLOR_STATE = 4;
   
  }  else if (mouseX > 360 && mouseX < 375 && mouseY > SCREEN_HEIGHT+4 && mouseY < SCREEN_HEIGHT+19) {
    // None blue  
    COLOR_STATE = 2;
   
  }  else if (mouseX > 360 && mouseX < 375 && mouseY > SCREEN_HEIGHT+22 && mouseY < SCREEN_HEIGHT+37) {
    // All blue  
    COLOR_STATE = 5;
   
  }  else if (mouseX > 380 && mouseX < 395 && mouseY > SCREEN_HEIGHT+4 && mouseY < SCREEN_HEIGHT+19) {
    // None green  
    COLOR_STATE = 3;
   
  }  else if (mouseX > 380 && mouseX < 395 && mouseY > SCREEN_HEIGHT+22 && mouseY < SCREEN_HEIGHT+37) {
    // All green  
    COLOR_STATE = 6;
  }
}

// r,g,b values are from 0 to 255
// h = [0,360], s = [0,1], v = [0,1]
// if s == 0, then h = -1 (undefined)
// 
// code from http://www.cs.rit.edu/~ncs/color/t_convert.html

RGBColor RGBtoHSV(RGBColor rgb)
{
  float h,s,v;
  
  float r = rgb.r/float(255);
  float g = rgb.g/float(255);
  float b = rgb.b/float(255);
  
  float MIN = min(r, min(g,b));  // min(r,g,b)
  float MAX = max(r, max(g,b));  // max(r,g,b)
 
  v = MAX;            // v

  float delta = MAX - MIN;

  if (MAX != 0 ) s = delta / MAX;  // s
  else { // r = g = b = 0    // s = 0, v is undefined
    s = 0;
    h = -1;
    return new RGBColor(h,s,v);
  }
  if( r == MAX ) h = 60.0 * ( g - b ) / delta; // between yellow & magenta
  else {
    if( g == MAX ) {
      h = 120.0 + 60.0 * ( b - r ) / delta; // between cyan & yellow
    } else {
      h = 240.0 + 60.0 * ( r - g ) / delta;  // between magenta & cyan
    }
  }
  if( h < 0 ) h += 360;
  
  return new RGBColor(h,s,v);
}

// r,g,b values are from 0 to 255
// h = [0,360], s = [0,1], v = [0,1]
// if s == 0, then h = -1 (undefined)
//
// code from http://www.cs.rit.edu/~ncs/color/t_convert.html

RGBColor HSVtoRGB(RGBColor hsv)
{
  int i;
  float r, g, b, f, p, q, t;
  float h = hsv.r;
  float s = hsv.g;
  float v = hsv.b;
  
  if( s == 0 ) {
    // achromatic (grey)
    r = g = b = (v*255);
    return new RGBColor(r,g,b);
  }
  
  h /= 60;      // sector 0 to 5
  i = floor( h );
  f = h - i;      // factorial part of h
  p = v * ( 1 - s );
  q = v * ( 1 - s * f );
  t = v * ( 1 - s * ( 1 - f ) );
  
  switch( i ) {
    case 0:
      r = v * 255;
      g = t * 255;
      b = p * 255;
      break;
    case 1:
      r = q * 255;
      g = v * 255;
      b = p * 255;
      break;
    case 2:
      r = p * 255;
      g = v * 255;
      b = t * 255;
      break;
    case 3:
      r = p * 255;
      g = q * 255;
      b = v * 255;
      break;
    case 4:
      r = t * 255;
      g = p * 255;
      b = v * 255;
      break;
    default:    // case 5:
      r = v * 255;
      g = p * 255;
      b = q * 255;
      break;
  }
  return new RGBColor(r,g,b); 
}

//
// get_index
//
// Return the index in the pixelarray given an (x,y) coordinate
int get_index(Coord coord) {
  return coord.x + (coord.y * ROW_WIDTH);
}

// Calculates an individual hex's height and width
// Calculates the cropped dimensions of the image

void CalcPixelParameters(float imageWidth, float imageHeight) {
  
  // Figure out whether image's height or width is too big
  // imgWidth, imgHeight are globals (boo!) that represent cropped width and height
  if ((imageWidth / imageHeight) > widthheight) {
    // Image is too wide - scale down
    imgWidth = (int)(imageHeight * widthheight);
    imgHeight = (int)imageHeight;
  } else {
    // Image is too tall - scale down
    imgWidth = (int)imageWidth;
    imgHeight = (int)(imageWidth / widthheight);
  }
  
  //
  // Figure out start and ending height and width coordinates
  //
  // Center is (imageWidth/2, imageHeight/2)
  //
  if (vertcenter) {  // Center the image vertically
    startWidth = (int)((imageWidth / 2) - (imgWidth / 2));
    endWidth = (int)((imageWidth / 2) + (imgWidth / 2));
  } else {
    startWidth = 0;  // Take just the left part of the image
    endWidth = (int)imgWidth;
  }
  
  if (horizcenter) {  // Center the image horizontally
    startHeight = (int)((imageHeight / 2) - (imgHeight / 2));
    endHeight = (int)((imageHeight / 2) + (imgHeight / 2));
  } else {
    startHeight = 0;  // Take jsut the top of the image
    endHeight = (int)imgHeight;
  }
}

// Find the triangle coordinate of an x,y point

Coord GetPixelCoord(int x, int y, int imageHeight, int imageWidth) {
  float pix_height = imageHeight / TRI_GEN;
  float pix_width = imageWidth / (TRI_GEN*2);
  
  // y is easy. Flip in direction between processing and triangles have different 0's
  int coord_y = (int)(y / pix_height);
  int remain_y = y % round(pix_height);
  
  coord_y = TRI_GEN - coord_y - 1;
  
  // x is harder - Needs improvemnt
  int coord_x = (int)(x / pix_width);
  int remain_x = x % round(pix_width);
  
  if ((coord_x + coord_y) % 2 == 0) {
    coord_x += bin_upward_diag(remain_x,remain_y,pix_width,pix_height);  // evens
  } else {
    coord_x += bin_downward_diag(remain_x,remain_y,pix_width,pix_height);  // odds
  }
  return (new Coord(coord_x,coord_y));
}

//
// bin_upward_diag
//
// is the x value to the left or right of the diagonal made by
// drawing a line from (0,0) to (x2,y2)
// return -1 for left, 0 for right
int bin_upward_diag(int x, int y, float x2, float y2) {
  float x_line = y * x2/y2;
  if (x > x_line) {
    return 1;
  } else {
    return 0;
  }
}

//
// bin_downward_diag
//
// is the x value to the left or right of the diagonal made by
// drawing a line from (0,y2) to (x2,0)
// return -1 for left, 0 for right
int bin_downward_diag(int x, int y, float x2, float y2) {
  float x_line = x2 - ((x2 * y) / y2);
  if (x > x_line) {
    return 1;
  } else {
    return 0;
  }
}

// Get helper functions
//
// Makes code more readable
// No out-of-bounds error handling. Make sure grid# is valid!
int getBigX(int grid) { return (BigTriCoord[grid][0]); }
int getBigY(int grid) { return (BigTriCoord[grid][1]); }
char getConnector(int grid) { return (connectors[grid][0]); }
char getLightDir(int grid) { return (connectors[grid][1]); }

//
// minBigX
//
// Smallest BigX value
int minBigX() {
  int min_x = getBigX(0);
  for (int i=1; i<numBigTri; i++) {
    if (getBigX(i) < min_x) min_x = getBigX(i);
  }
  return min_x;
}

//
// minBigY
//
// Smallest BigY value
int minBigY() {
  int min_y = getBigY(0);
  for (int i=1; i<numBigTri; i++) {
    if (getBigY(i) < min_y) min_y = getBigY(i);
  }
  return min_y;
}

//
// grid_width
//
// How many triangles across is the big grid?
float grid_width() {
  
  if (TILING == false) return 1;  // Want just one grid
  
  int min_x = getBigX(0);
  int max_x = min_x;
  int new_x;
  
  for (int i=1; i<numBigTri; i++) {
    new_x = getBigX(i);
    if (new_x < min_x) min_x = new_x;
    if (new_x > max_x) max_x = new_x;
  }
  return (max_x - min_x + 2) / 2.0;  // 2 is because of up/down
}

//
// grid_height
//
// How many triangles high is the big grid?
int grid_height() {
  
  if (TILING == false) return 1;
  
  int min_y = getBigY(0);
  int max_y = min_y;
  int new_y;
  
  for (int i=1; i<numBigTri; i++) {
    new_y = getBigY(i);
    if (new_y < min_y) min_y = new_y;
    if (new_y > max_y) max_y = new_y;
  }
  return (max_y - min_y + 1);
}

//
// IsCoordinGrid
//
// Checks to see whether (x,y) is in the grid specified
boolean IsCoordinGrid(int x, int y, int grid) {
  // Check grid bounds
  if (grid < 0 || grid >= numBigTri) {
    return (false);
  }
  
  // Correct for big-grid offsets
  x -= getBigX(grid) * TRI_GEN;
  y -= getBigY(grid) * TRI_GEN;
  
  if (!isPointUp(getBigX(grid),getBigY(grid))) {
    y = TRI_GEN - y - 1;
  }
  // Check y-row first
  if (y < 0 || y >= TRI_GEN) {
   return (false);  // y is out of bounds
  }
  // Check x-column
  if (x < y || x >= y + rowWidth(y)) {
    return (false);  // x is out of bounds
  }
  
  return (true);
}

//
// Converts an x,y triangle coordinate into a light number
// for grid number grid
//

int GetLightFromCoord(int x, int y, int grid) {
  if (IsCoordinGrid(x,y,grid) == false) {
    print(x,y,grid);
    return (NONE);
  }
  
  int light = 0;  // LED number
  int rowflip;  // Whether the row flips order
  
  // Remove big-grid offsets
  // Correct for big-grid offsets
  x -= getBigX(grid) * TRI_GEN;
  y -= getBigY(grid) * TRI_GEN;
  
  boolean pointUp = isPointUp(getBigX(grid), getBigY(grid));
  char connector = getConnector(grid);
  char light_dir = getLightDir(grid);
  
  // Downward pointing grids are bizarre
  if (!pointUp) {
    y = TRI_GEN - y - 1;
    // Swap the light direction: L -> R and R -> L
    if (light_dir == 'L') {
      light_dir = 'R';
    } else {
      light_dir = 'L';
    }
  }
  
  if (light_dir == 'R') { // Left-right direction of wiring
    rowflip = 1;
  } else {
    rowflip = 0;
  }
  
  // y row coordinate first. We're building up LEDs one row at a time.
  for (int row = 0; row < y; row++) {
    light += rowWidth(row);
  }
  // add x column coordinate
  // Even rows serpentine back
  if (y % 2 == rowflip) {  // even
    light += rowWidth(y) - (x-y) - 1;
  } else {  // odd
    light += (x-y);
  }
  
  // Coordinate transformation depending on how the Triangle is hung
  switch (connector) {  // Which corner (Left/center/right) for the connector
    case 'C':  // connector at top corner
      return rotateclock[light];
    case 'R':  // connector at bottom right corner
      if (light_dir == 'L') {
        return light;
      } else {
        return rotatecounter[light];
      }
    default:  // case 2: connector at bottom left corner
      if (light_dir == 'L') {
        return rotatecounter[light];
      } else {
        return light;
      }
  }
}

// isPointUp
//
// Given an (x,y) coordinate, does a triangle point up?
// Add x+y. Evens point up, odds point down.
// Works for the Big Triangle coordinates as well
boolean isPointUp(int x, int y) {
  if ((x+y) % 2 == 0) {
    return (true);
  } else {
    return (false);
  }
}

// How many lights on a row?

int rowWidth(int row) {
  return ((TRI_GEN-row-1)*2)+1;
}

TriForm makeTriGrid(int big_x, int big_y, int big_num) {
  
  TriForm form = new TriForm();
  
  boolean up = isPointUp(big_x,big_y);
   
  // small triangle coordinate offsets 
  int x_offset = big_x * TRI_GEN;
  int y_offset = big_y * TRI_GEN;
  if(!up) y_offset += (TRI_GEN-1);  // Move to top-left corner
  
  // screen pixel offsets
  int pix_x_offset = CORNER_X + ((big_x - minBigX()) * BASE / 2);  
  int pix_y_offset = CORNER_Y - ((big_y - minBigY()) * BIG_HEIGHT);
  if (!up) pix_y_offset -= ((TRI_GEN-1) * TRI_HEIGHT);
  
  for (int y=0; y<TRI_GEN; y++) {  // rows
    for (int x=0; x<rowWidth(y); x++) {  // columns
      // Calculate where to draw the pixel triangle on the screen
      int pix_x = (int)(pix_x_offset + (TRI_SIZE/2 * (x+y)));
      int pix_y = pix_y_offset;
      
      if (up) {
        pix_y -= (int)(y * TRI_HEIGHT);
      } else {
        pix_y += (int)(y * TRI_HEIGHT);
      }
      // Calculate pixel coordinates based on column and row
      int xcoord = x_offset + x + y;
      int ycoord = y_offset;
      if (up) {
        ycoord += y;
      } else {
        ycoord -= y;
      }
      form.add(new Tri(pix_x,pix_y, xcoord,ycoord, big_num));
    }
  }
  return form;  
}


class TriForm {
  ArrayList<Tri> tris;
  
  TriForm() {
    tris = new ArrayList<Tri>();
  }
  
  void add(Tri t) {
    int triId = tris.size();
    tris.add(t);
  }
  
  int size() {
    return tris.size();
  }
  
  void draw() {
    for (Tri t : tris) {
      t.draw();
    }
  }
  
  // Reworked for iterative search (SD) XXX probably need a better API here!
  void setCellColor(color c, int i) {
    if (i >= tris.size()) {
      println("invalid offset for TriForm.setColor: i only have " + tris.size() + " triangles");
      return;
    }
    for (Tri t : tris) {  // Search all 
      if (i == t.LED) {  // for the one that has the correct LED#
        t.setColor(c);
        return;
      }
    }
    println("Could not find LED #"+i);
  }
    
}

/*
 *  Triangle shape primitives
 */

public float triHeight(int size) {
  return sqrt(3)/2 * size;
}


class Tri {
  String id = null; // "xcoord, ycoord"
  int x;  // x-coordinate in pixels on the screen
  int y;  // y-coordinate in pixels on the screen
  int xcoord;  // x in the triangle array (column)
  int ycoord;  // y in the triangle array (row)
  int big_num; // strip number
  int LED;     // LED number on the strand
  color c;
  
  Tri(int pix_x, int pix_y, int xcoord, int ycoord, int big_num) {
    this.x = pix_x;
    this.y = pix_y;
    this.xcoord = xcoord;
    this.ycoord = ycoord;
    this.big_num = big_num;
    this.LED = GetLightFromCoord(this.xcoord, this.ycoord, big_num);
    this.c = color(255,255,255);
    
    // str(xcoord + ", " + ycoord)
    int[] coords = new int[2];
    coords[0] = xcoord;
    coords[1] = ycoord;
    this.id = join(nf(coords, 0), ",");
  }

  void setId(String id) {
    this.id = id;
  }
  
  void setColor(color c) {
    this.c = c;
  }

  void draw() {
    fill(c);
    stroke(0);
    
    boolean up = isPointUp(xcoord,ycoord);
    drawTriangle(x,y,(int)TRI_SIZE,up);
    
    // toggle text label between light number and x,y coordinate
    String text = "";
    switch (DRAW_LABELS) {
      case 0:
        // string(grid# + ", " + LED#)
        int[] coords = new int[2];
        coords[0] = this.big_num;
        coords[1] = this.LED;
        text = join(nf(coords, 0), ",");
        break;
      case 1:
        text = this.id;  // (x,y) coordinate
        break;
      case 2:
        // no label
        break;
    }
    
    if (this.id != null) {
      fill(0);
      textAlign(CENTER);
      
      if (up) {
        text(text, this.x + TRI_SIZE/2, this.y - TRI_HEIGHT/5);
      } else {
        text(text, this.x + TRI_SIZE/2, this.y - TRI_HEIGHT/2);
      }
    }
    noFill();
  }
}

//
// drawBigFrame
//
// Draws a big bold triangle around each grid

void drawBigFrame(int grid) {
  // Check bounds
  if (grid < 0 || grid > numBigTri) return;  // Out of bounds
  
  int x = getBigX(grid);
  int y = getBigY(grid);
  int x_coord = CORNER_X + ((x-minBigX()) * BASE/2);
  int y_coord = CORNER_Y - ((y-minBigY()) * BIG_HEIGHT);
  
  noFill();
  strokeWeight(5);
  drawTriangle(x_coord,y_coord,BASE,isPointUp(x,y));
  strokeWeight(1);
  
  if (DRAW_LABELS == 0) {
    // Draw the connector point as a red triangle
    boolean up = isPointUp(getBigX(grid),getBigY(grid));
    int point = 1;  // down
    if (up) point = 0;
    
    fill(255,0,0);  // Red Triangle
    // Sorry for the mess below
    switch (getConnector(grid)) {
      case 'L':
        drawTriangle(x_coord, (int)(y_coord-(point * (BIG_HEIGHT-TRI_SIZE))), (int)TRI_SIZE, up);
        break;
      case 'C':
        drawTriangle((int)(x_coord+(BASE/2)-(TRI_SIZE/2)), (int)(y_coord-BIG_HEIGHT+TRI_SIZE+(point * (BIG_HEIGHT-TRI_SIZE))), (int)TRI_SIZE, up);
        break;
      default:
        drawTriangle((int)(x_coord+BASE-TRI_SIZE), (int)(y_coord - (point * (BIG_HEIGHT-TRI_SIZE))), (int)TRI_SIZE, up);
        break;
    }
  }
}

//
// drawTriangle(x,y,size,pointUp);
//
// Draws an equilateral triangle from x,y
// If pointed down, (x,y) is lower left "corner" outside the triangle
void drawTriangle(int x, int y, int size, boolean up) {
  int Height = (int)triHeight(size);
  
  if (up) {  // "Delta" drawn from lower left corner
    triangle(x,y, x+size,y, x+(size/2), y-Height);
  } else {  // Inverted "delta" drawn from bottom point
    triangle(x+(size/2),y, x+size,y-Height, x,y-Height);
  }
}

//
//  Routines to interact with the Lights
//

void movePixelsToBuffer() {
  for (int y=0; y<TRI_GEN; y++) {  // rows
    for (int x=0; x<rowWidth(y); x++) {  // columns
      for (int tri=0; tri<numBigTri; tri++) {
        // Get rgb values from binned hex
        Coord coord = new Coord(x+y,y);
        if (coord.outofbounds()) continue;  // Memory fault
        int pix = GetLightFromCoord(coord.x,coord.y,0);  // Works!
        if (!isPointUp(getBigX(tri),getBigY(tri))) {  // Gotta rotate the image for point down triangles
          pix = rotateclock[pix];
        }
        RGBColor rgb = pixelarray.Pixels[get_index(coord)].pixcolor;
        int r = (int)rgb.r;
        int g = (int)rgb.g;
        int b = (int)rgb.b;
        
        setPixelBuffer(tri, pix, r,g,b);  // Lights
        triGrid[tri].setCellColor(color(r,g,b), pix);  // Simulator 
      }
    }
  }
}
        
void sendDataToLights() {
  
  int BigTri, pixel;
  
  if (testObserver.hasStrips) {   
    registry.startPushing();
    registry.setExtraDelay(0);
    registry.setAutoThrottle(true);
    registry.setAntiLog(true);    
    
    List<Strip> strips = registry.getStrips();
    BigTri = 0;
    
    for (Strip strip : strips) {      
      for (pixel = 0; pixel < (TRI_GEN*TRI_GEN); pixel++) {
         if (hasChanged(BigTri,pixel)) {
           strip.setPixel(getPixelBuffer(BigTri,pixel), pixel);
         }
      }
      BigTri++;
      if (BigTri >=numBigTri) break;  // Prevents buffer overflow
    }
  }
}

void initializeColorBuffers() {
  for (int t = 0; t < numBigTri; t++) {
    for (int p = 0; p < NUM_PIXELS; p++) {
      curr_buffer[t][p][0] = 100;
      curr_buffer[t][p][1] = 100;
      curr_buffer[t][p][2] = 100;
      setPixelBuffer(t, p, 0,0,0);
    }
  }
  sendDataToLights();
  pushColorBuffer();
  println("go!");
}

void forceBlack() {
  for (int t = 0; t < numBigTri; t++) {
    for (int p = 0; p < NUM_PIXELS; p++) {
      curr_buffer[t][p][0] = 100;
      curr_buffer[t][p][1] = 100;
      curr_buffer[t][p][2] = 100;
      setPixelBuffer(t, p, 0,0,0);  // Lights
    }
    for (int p = 0; p < TRI_GEN*TRI_GEN; p++) {
      triGrid[t].setCellColor(color(0,0,0), p);  // Simulator
    }
  }
  sendDataToLights();
  pushColorBuffer();
}

void setPixelBuffer(int BigTri, int pixel, int r, int g, int b) {
  BigTri = bounds(BigTri, 0, numBigTri-1);
  pixel = bounds(pixel, 0, NUM_PIXELS-1);
  
  next_buffer[BigTri][pixel][0] = r;
  next_buffer[BigTri][pixel][1] = g;
  next_buffer[BigTri][pixel][2] = b;
}

color getPixelBuffer(int BigTri, int pixel) {
  BigTri = bounds(BigTri, 0, numBigTri-1);
  pixel = bounds(pixel, 0, NUM_PIXELS-1);
  
  return color(next_buffer[BigTri][pixel][0],
               next_buffer[BigTri][pixel][1],
               next_buffer[BigTri][pixel][2]);
}

boolean hasChanged(int t, int p) {
  if (curr_buffer[t][p][0] != next_buffer[t][p][0] ||
      curr_buffer[t][p][1] != next_buffer[t][p][1] ||
      curr_buffer[t][p][2] != next_buffer[t][p][2]) {
        return true;
      } else {
        return false;
      }
}

void pushColorBuffer() {
  for (int t = 0; t < numBigTri; t++) {
    for (int p = 0; p < NUM_PIXELS; p++) {
      curr_buffer[t][p][0] = next_buffer[t][p][0];
      curr_buffer[t][p][1] = next_buffer[t][p][1];
      curr_buffer[t][p][2] = next_buffer[t][p][2]; 
    }
  }
}

int bounds(int value, int minimun, int maximum) {
  if (value < minimun) return minimun;
  if (value > maximum) return maximum;
  return value;
}

private void prepareExitHandler () {

  Runtime.getRuntime().addShutdownHook(new Thread(new Runnable() {

    public void run () {

      System.out.println("Shutdown hook running");

      List<Strip> strips = registry.getStrips();
      for (Strip strip : strips) {
        for (int i=0; i<strip.getLength(); i++)
          strip.setPixel(#000000, i);
      }
      for (int i=0; i<100000; i++)
        Thread.yield();
    }
  }
  ));
}
