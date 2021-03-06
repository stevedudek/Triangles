
/*

  Triangle Simulator and Lighter
  
  1. Simulator: draws triangles on the monitor
  2. Lighter: sends data to the lights
  
  Includes Tiling of Multiple Big Triangle Grids
  
  DUAL SHOWS - Works!
  
  HSV colors (not RGB) for better interpolation
  
  1/11/18
  
  Main parameter is triangle TRI_GEN, or number of triangles on the base
  TRI_GEN is fixed at 12 for 144 total triangles.
  
  x,y coordinates are weird for each triangle, but selected to make
  both neighbors and linear movement easier. Turn on the coordinates
  to see the system.
  
  Number of Big Triangles set by NUM_BIG_TRI. Each Big Triangles needs
  an (x,y) coordinate and a (L,R) connector designation.
  
*/

int NUM_BIG_TRI = 6;  // Number of Big Triangles

// Relative coordinates for the Big Triangles
int[][] BigTriCoord = {
  {0,0},  // Strip 1
  {1,1},  // Strip 2
  {2,0},  // Strip 3
  {4,0},  // Strip 4
  {5,1},  // Strip 5
  {6,0},  // Strip 6
};

// Matrix listing where the connector attaches physically
// to each Big Triangle.
// First value is Corner (Pixel 0) of connector attachment
// 'L' = Left, 'R' = Right, 'C' = Center
// Second value is Direction of lights (0->1) from connector
// as viewed from corner
// 'L' = Left, 'R' = Right
char[][] connectors = {
  {'L','L'},  // Strip 1
  {'L','L'},  // Strip 2
  {'L','L'},  // Strip 3
  {'L','L'},  // Strip 4
  {'L','L'},  // Strip 5
  {'L','L'}   // Strip 6
};

import com.heroicrobot.dropbit.registry.*;
import com.heroicrobot.dropbit.devices.pixelpusher.Pixel;
import com.heroicrobot.dropbit.devices.pixelpusher.Strip;
import com.heroicrobot.dropbit.devices.pixelpusher.PixelPusher;
import com.heroicrobot.dropbit.devices.pixelpusher.PusherCommand;

import processing.net.*;
import java.util.*;
import java.util.regex.*;
import java.awt.Color;

int NUM_CHANNELS = 2;  // Dual shows

// network vars
int port = 4444;
Server[] _servers = new Server[NUM_CHANNELS];  // For dual shows 
StringBuffer[] _bufs = new StringBuffer[NUM_CHANNELS];  // separate buffers

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
Strip[] strip_array = new Strip[NUM_BIG_TRI];

int NONE = 9999;  // hack: "null" for "int'

//
// Controller on the bottom of the screen
//
// Draw labels has 3 states:
// 0:LED number, 1:(x,y) coordinate, and 2:none
int DRAW_LABELS = 2;

boolean UPDATE_VISUALIZER = true;  // turn false for LED-only updates

int BRIGHTNESS = 100;  // A percentage

int COLOR_STATE = 0;  // No enum types in processing. Messy

// How many little triangles on the base of each big triangle
int TRI_GEN = 12;  // Don't change
int NUM_PIXELS = TRI_GEN * TRI_GEN;  // Don't change

// Color buffers: [BigTri][Pixel][hsv color]
int buff_width = (int)(grid_width() * TRI_GEN * 2);  // x axis for buffer
int buff_height = (int)(grid_height() * TRI_GEN);  // y axis for buffer
color[][][] curr_buffer = new color[NUM_CHANNELS][NUM_BIG_TRI][NUM_PIXELS];
color[][][] next_buffer = new color[NUM_CHANNELS][NUM_BIG_TRI][NUM_PIXELS];
color[][][] morph_buffer = new color[NUM_CHANNELS][NUM_BIG_TRI][NUM_PIXELS];  // blend of curr + next
color[][] interp_buffer = new color[NUM_BIG_TRI][NUM_PIXELS];  // combine two channels here

// Timing variables needed to control regular morphing
// Doubled for 2 channels
int[] delay_time = { 10000, 10000 };  // delay time length in milliseconds (dummy initial value)
long[] start_time = { millis(), millis() };  // start time point (in absolute time)
long[] last_time = { start_time[0], start_time[1] };
short[] channel_intensity = { 255, 0 };  // Off = 0, All On = 255 

// Calculated pixel constants for simulator display
int SCREEN_SIZE = 700;  // square screen
float TRI_SIZE = (SCREEN_SIZE - 20) / (TRI_GEN * grid_width());  // Scale triangles to fit screen
float TRI_HEIGHT = TRI_SIZE * 0.866;
int BASE = (int)(TRI_GEN * TRI_SIZE);  // Width of big triangle
int BIG_HEIGHT = (int)triHeight(BASE);  // Height of big triangle
int SCREEN_WIDTH = (int)(BASE * grid_width()) + 20;  // Width + a little
int SCREEN_HEIGHT = (BIG_HEIGHT * grid_height()) + 20; // Height + a little
int CORNER_X = 10; // bottom left corner position on the screen
int CORNER_Y = SCREEN_HEIGHT - 10; // bottom left corner position on the screen

// Grid model(s) of Big Triangles
TriForm[] triGrid = new TriForm[NUM_BIG_TRI];

PFont font_triangle = createFont("Helvetica", 12, true);

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

//
// Helper classes: Coord
//
class Coord {
  public int x, y;
  
  Coord(int x, int y) {
    this.x = x;
    this.y = y;
  }
}

//
// setup
//
void setup() {
  
  size(SCREEN_WIDTH, SCREEN_HEIGHT + 50); // 50 for controls
  stroke(0);
  fill(255,255,0);
  
  frameRate(20);
  
  // Set up the Big Triangles and stuff in the little triangles
  for (int i = 0; i < NUM_BIG_TRI; i++) {
    triGrid[i] = makeTriGrid(getBigX(i), getBigY(i), i);
  }
  
  // Pixel Pusher stuff
  registry = new DeviceRegistry();
  testObserver = new TestObserver();
  registry.addObserver(testObserver);
  prepareExitHandler();
  strips = registry.getStrips();
  
  colorMode(HSB, 255);  // HSB colors (not RGB)
  
  initializeColorBuffers();  // Stuff curr/next frames with zeros (all black)
  
  background(0, 0, 200);  // gray
  
  for (int i = 0; i < NUM_CHANNELS; i++) {
    _bufs[i] = new StringBuffer();
    _servers[i] = new Server(this, port + i);
    println("server " + i + " listening: " + _servers[i]);
  }
}

//
// Draw - Main function
//
void draw() {
  drawBottomControls();
  pollServer();        // Get messages from python show runner
  update_morph();      // Morph between current frame and next frame
  interpChannels();    // Update the visualizer
  if (UPDATE_VISUALIZER) {
    drawTriangles();     // Re-draw frames and triangles
  }
  sendDataToLights();  // Dump data into lights
  print_memory_usage();
}

void drawTriangles() {  
  for (int i = 0; i < NUM_BIG_TRI; i++) {
    triGrid[i].draw();  // Draw each grid
    drawBigFrame(i);    // Draw a bold frame around each grid
  }
  if (DRAW_LABELS == 0) {
    drawGuides();  // Draw the red guides
  }
}

//
// Bottom Control functions
//
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
  fill(0,0,255);
  rect(0,SCREEN_HEIGHT,SCREEN_WIDTH,40);
  
  // draw divider lines
  stroke(0);
  line(140,SCREEN_HEIGHT,140,SCREEN_HEIGHT+40);
  line(290,SCREEN_HEIGHT,290,SCREEN_HEIGHT+40);
  line(470,SCREEN_HEIGHT,470,SCREEN_HEIGHT+40);
  
  // draw checkboxes
  stroke(0);
  fill(0,0,255);
  
  // Checkbox is always unchecked; it is 3-state
  rect(20,SCREEN_HEIGHT+10,20,20);  // label checkbox
  
  rect(200,SCREEN_HEIGHT+4,15,15);  // plus brightness
  rect(200,SCREEN_HEIGHT+22,15,15);  // minus brightness
  
  drawCheckbox(340,SCREEN_HEIGHT+4,15, color(255,255,255), COLOR_STATE == 1);  // None Red
  drawCheckbox(340,SCREEN_HEIGHT+22,15, color(255,255,255), COLOR_STATE == 4);  // All Red
  drawCheckbox(360,SCREEN_HEIGHT+4,15, color(87,255,255), COLOR_STATE == 2);  // None Blue
  drawCheckbox(360,SCREEN_HEIGHT+22,15, color(87,255,255), COLOR_STATE == 5);  // All Blue
  drawCheckbox(380,SCREEN_HEIGHT+4,15, color(175,255,255), COLOR_STATE == 3);  // None Green
  drawCheckbox(380,SCREEN_HEIGHT+22,15, color(175,255,255), COLOR_STATE == 6);  // All Green
  
  drawCheckbox(400,SCREEN_HEIGHT+10,20, color(0,0,255), COLOR_STATE == 0);  
  
  // draw text labels in 12-point Helvetica
  fill(0);
  textAlign(LEFT);
  
  textFont(font_triangle, 12);  
  text("Toggle Labels", 50, SCREEN_HEIGHT+25);
  text("+", 190, SCREEN_HEIGHT+16);
  text("-", 190, SCREEN_HEIGHT+34);
  text("Brightness", 225, SCREEN_HEIGHT+25);
  textFont(font_triangle, 20);
  text(BRIGHTNESS, 150, SCREEN_HEIGHT+28);
  
  textFont(font_triangle, 12);
  text("None", 305, SCREEN_HEIGHT+16);
  text("All", 318, SCREEN_HEIGHT+34);
  text("Color", 430, SCREEN_HEIGHT+25); 
}

void mouseClicked() {  
  //println("click! x:" + mouseX + " y:" + mouseY);
  if (mouseX > 20 && mouseX < 40 && mouseY > SCREEN_HEIGHT+10 && mouseY < SCREEN_HEIGHT+30) {
    // clicked draw labels button
    DRAW_LABELS = (DRAW_LABELS + 1) % 3;
   
  }  else if (mouseX > 200 && mouseX < 215 && mouseY > SCREEN_HEIGHT+4 && mouseY < SCREEN_HEIGHT+19) {
    // Bright up checkbox
    if (BRIGHTNESS <= 95) BRIGHTNESS += 5;
    
   
  } else if (mouseX > 200 && mouseX < 215 && mouseY > SCREEN_HEIGHT+22 && mouseY < SCREEN_HEIGHT+37) {
    // Bright down checkbox
    BRIGHTNESS -= 5;  
    if (BRIGHTNESS < 1) BRIGHTNESS = 1;
  
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

//
// Get helper functions
//
// Makes code more readable
// No out-of-bounds error handling. Make sure grid# is valid!
int getBigX(int grid) { return (BigTriCoord[grid][0]); }
int getBigY(int grid) { return (BigTriCoord[grid][1]); }
char getConnector(int grid) { return (connectors[grid][0]); }
char getLightDir(int grid) { return (connectors[grid][1]); }

//
// minBigX - Smallest BigX value
//
int minBigX() {
  int min_x = getBigX(0);
  for (int i = 1; i < NUM_BIG_TRI; i++) {
    if (getBigX(i) < min_x) {
      min_x = getBigX(i);
    }
  }
  return min_x;
}

//
// minBigY - Smallest BigY value
// 
int minBigY() {
  int min_y = getBigY(0);
  for (int i = 1; i < NUM_BIG_TRI; i++) {
    if (getBigY(i) < min_y) {
      min_y = getBigY(i);
    }
  }
  return min_y;
}

//
// grid_width - How many triangles across is the big grid?
//
float grid_width() {
  int min_x = getBigX(0);
  int max_x = min_x;
  int new_x;
  
  for (int i=1; i < NUM_BIG_TRI; i++) {
    new_x = getBigX(i);
    if (new_x < min_x) { min_x = new_x; }
    if (new_x > max_x) { max_x = new_x; }
  }
  return (max_x - min_x + 2) / 2.0;  // 2 is because of up/down
}

//
// grid_height - How many triangles high is the big grid?
//
int grid_height() {
  int min_y = getBigY(0);
  int max_y = min_y;
  int new_y;
  
  for (int i = 1; i < NUM_BIG_TRI; i++) {
    new_y = getBigY(i);
    if (new_y < min_y) { min_y = new_y; }
    if (new_y > max_y) { max_y = new_y; }
  }
  return (max_y - min_y + 1);
}

//
// IsCoordinGrid - Checks to see whether (x,y) is in the grid specified
// 
boolean IsCoordinGrid(int x, int y, int grid) {
  // Check grid bounds
  if (grid < 0 || grid >= NUM_BIG_TRI) {
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
  if (IsCoordinGrid(x,y,grid) == false) return (NONE);
  
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

//
// isPointUp
//
// Given an (x,y) coordinate, does a triangle point up?
// Add x+y. Evens point up, odds point down.
// Works for the Big Triangle coordinates as well
boolean isPointUp(int x, int y) {
  return ((x+y) % 2 == 0);
}

//
// How many lights on a row?
//
int rowWidth(int row) {
  return ((TRI_GEN-row-1) * 2) + 1;
}

TriForm makeTriGrid(int big_x, int big_y, int big_num) {
  
  TriForm form = new TriForm(TRI_GEN * TRI_GEN);
  
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
      int led = GetLightFromCoord(xcoord, ycoord, big_num);
      form.add(new Tri(pix_x,pix_y, xcoord,ycoord, big_num, led), led);
    }
  }
  return form;  
}


class TriForm {
  Tri[] tris;
  int size;
  
  TriForm(int num_pixels) {
    tris = new Tri[num_pixels];
    this.size = num_pixels;
  }
  
  void add(Tri t, int led) {
    if (led < this.size) {
      this.tris[led] = t;
    }
  }
  
  void draw() {
    for (int i = 0; i < this.size; i++) {
      this.tris[i].draw();
    }
  }
  
  void setCellColor(color c, int i) {
    if (i < this.size) {
      this.tris[i].setColor(c);
    }
  }    
}

//
//  Triangle shape primitives
//
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
  
  Tri(int pix_x, int pix_y, int xcoord, int ycoord, int big_num, int led) {
    this.x = pix_x;
    this.y = pix_y;
    this.xcoord = xcoord;
    this.ycoord = ycoord;
    this.big_num = big_num;
    this.LED = led;
    this.c = color(255, 255, 255);
    
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
    drawTriangle(x, y, (int)TRI_SIZE, up);
    
    // toggle text label between light number and x,y coordinate
    String text = "";
    switch (DRAW_LABELS) {
      case 0:
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
// drawBigFrame - Draws a big bold triangle around each grid
//
void drawBigFrame(int grid) {
  // Check bounds
  if (grid < 0 || grid > NUM_BIG_TRI) return;  // Out of bounds
  
  int x = getBigX(grid);
  int y = getBigY(grid);
  int x_coord = CORNER_X + ((x-minBigX()) * BASE/2);
  int y_coord = CORNER_Y - ((y-minBigY()) * BIG_HEIGHT);
  
  noFill();
  strokeWeight(5);
  drawTriangle(x_coord,y_coord,BASE,isPointUp(x,y));
  strokeWeight(1);
}

//
// drawGuides
//
// Paints the first few pixels red of each Big Triangle
// as a way to check orientation
//
void drawGuides() {
  color RED = color(0, 255, 255);
  
  for (byte c = 0; c < NUM_CHANNELS; c++) {  // Do both channels
    for (byte t = 0; t < NUM_BIG_TRI; t++) {
      for (int p = 0; p < TRI_GEN; p++) {  // half a row
        triGrid[t].setCellColor(RED, p);  // Simulator
        next_buffer[c][t][p] = RED;  // Lights 
      }
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
//  Server Routines
//
void pollServer() {
  // Read 2 different server ports into 2 buffers - keep channels separated
  for (int i = 0; i < NUM_CHANNELS; i++) {
    try {
      Client c = _servers[i].available();
      // append any available bytes to the buffer
      if (c != null) {
        _bufs[i].append(c.readString());
      }
      // process as many lines as we can find in the buffer
      int ix = _bufs[i].indexOf("\n");
      while (ix > -1) {
        String msg = _bufs[i].substring(0, ix);
        msg = msg.trim();
        processCommand(msg);
        _bufs[i].delete(0, ix+1);
        ix = _bufs[i].indexOf("\n");
      }
    } catch (Exception e) {
      println("exception handling network command");
      e.printStackTrace();
    }
  }  
}

//
// With DUAL shows: 
// 1. all commands must start with either a '0' or '1'
// 2. Followed by either
//     a. X = Finish a morph cycle (clean up by pushing the frame buffers)
//     b. D(int) = delay for int milliseconds (but keeping morphing)
//     c. I(short) = channel intensity (0 = off, 255 = all on)
//     d. Otherwise, process 5 integers as (s,i, r,g,b)
//
//
void processCommand(String cmd) {
  if (cmd.length() < 2) { return; }  // Discard erroneous stub characters
  byte channel = (cmd.charAt(0) == '0') ? (byte)0 : (byte)1 ;  // First letter indicates Channel 0 or 1
  cmd = cmd.substring(1, cmd.length());  // Strip off first-letter Channel indicator
  
  if (cmd.charAt(0) == 'X') {  // Finish the cycle
    finishCycle(channel);
  } else if (cmd.charAt(0) == 'D') {  // Get the delay time
    delay_time[channel] = Integer.valueOf(cmd.substring(1, cmd.length()));
  } else if (cmd.charAt(0) == 'I') {  // Get the intensity
    channel_intensity[channel] = Integer.valueOf(cmd.substring(1, cmd.length())).shortValue();
  } else {  
    processPixelCommand(channel, cmd);  // Pixel command
  }
}

// 5 comma-separated numbers for triangle, pixel, h, s, v
Pattern cmd_pattern = Pattern.compile("^\\s*(\\d+),(\\d+),(\\d+),(\\d+),(\\d+)\\s*$");

void processPixelCommand(byte channel, String cmd) {
  Matcher m = cmd_pattern.matcher(cmd);
  if (!m.find()) {
    //println(cmd);
    println("ignoring input for " + cmd);
    return;
  }
  byte t    =    Byte.valueOf(m.group(1));
  int p     = Integer.valueOf(m.group(2));
  int h     = Integer.valueOf(m.group(3));
  int s     = Integer.valueOf(m.group(4));
  int v     = Integer.valueOf(m.group(5));
  
  next_buffer[channel][t][p] = color( (short)h, (short)s, (short)v );  
//  println(String.format("setting channel %d pixel:%d,%d to h:%d, s:%d, v:%d", channel, s, i, h, s, v));
}

//
// Finish Cycle
//
// Get ready for the next morph cycle by morphing to the max and pushing the frame buffer
//
void finishCycle(byte channel) {
  morph_frame(channel, 1.0);  // May work after all
  pushColorBuffer(channel);
  start_time[channel] = millis();  // reset the clock
}

//
// Update Morph
//
void update_morph() {
  // Fractional morph over the span of delay_time
  for (byte channel = 0; channel < NUM_CHANNELS; channel++) {
    last_time[channel] = millis();  // update clock
    float fract = (last_time[channel] - start_time[channel]) / (float)delay_time[channel];
    if (is_channel_active(channel) && fract <= 1.0) {
      morph_frame(channel, fract);
    }
  }
}

//
// Is Channel Active
//
boolean is_channel_active(int channel) {
  return (channel_intensity[channel] > 0);
}


/////  Routines to interact with the Lights

//
// Interpolate Channels
//
// Interpolate between the 2 channels
// Push the interpolated results on to the simulator 
//
void interpChannels() {
  if (!is_channel_active(0)) {
    pushOnlyOneChannel(1);
  } else if (!is_channel_active(1)) {
    pushOnlyOneChannel(0);
  } else {
    float fract = (float)channel_intensity[0] / (channel_intensity[0] + channel_intensity[1]);
    morphBetweenChannels(fract);
  }
}

//
// pushOnlyOneChannel - push the morph_channel to the simulator
//
void pushOnlyOneChannel(int channel) {
  color col;
  for (byte t = 0; t < NUM_BIG_TRI; t++) {
    for (int p = 0; p < NUM_PIXELS; p++) {
      col = adjColor(morph_buffer[channel][t][p]);
      triGrid[t].setCellColor(col, p);
      interp_buffer[t][p] = col;
    }
  }
}

//
// morphBetweenChannels - interpolate the morph_channel on to the simulator
//
void morphBetweenChannels(float fract) {
  color col;
  for (byte t = 0; t < NUM_BIG_TRI; t++) {
    for (int p = 0; p < NUM_PIXELS; p++) {
      col = adjColor(interp_color(morph_buffer[1][t][p], morph_buffer[0][t][p], fract));
      triGrid[t].setCellColor(col, p);
      interp_buffer[t][p] = col;
    }
  }
}

// Adjust color for brightness and hue
color adjColor(color c) {
  return adj_brightness(colorCorrect(c));
}

// Convert hsb color (0-255) to hsb (0-1.0) and then to rgb (0-255)
//   warning: it's messy
color hsb_to_rgb(color c) {
  int color_int = Color.HSBtoRGB(hue(c) / 255.0,  // 255?
                                 saturation(c) / 255.0, 
                                 brightness(c) / 255.0);
  return color((color_int & 0x00FF0000) >> 16, 
               (color_int & 0x0000FF00) >> 8, 
               (color_int & 0x000000FF));
}

//
//  Routines for the strip buffer
//

void sendDataToLights() {
  byte t;
  int p;
  
  if (testObserver.hasStrips) {   
    registry.startPushing();
    registry.setExtraDelay(0);
    registry.setAutoThrottle(true);
    registry.setAntiLog(true);    
    
    List<Strip> strips = registry.getStrips();
    t = 0;
    
    for (Strip strip : strips) {      
      for (p = 0; p < NUM_PIXELS; p++) {
        strip.setPixel(hsb_to_rgb(interp_buffer[t][p]), p);
      }
      t++;
      if (t >= NUM_BIG_TRI) break;  // Prevents buffer overflow
    }
  }
}

private void prepareExitHandler () {

  Runtime.getRuntime().addShutdownHook(new Thread(new Runnable() {

    public void run () {

      System.out.println("Shutdown hook running");

      List<Strip> strips = registry.getStrips();
      for (Strip strip : strips) {
        for (int i = 0; i < strip.getLength(); i++)
          strip.setPixel(#000000, i);
      }
      for (int i=0; i<100000; i++)
        Thread.yield();
    }
  }
  ));
}

//
//  Fractional morphing between current and next frame - sends data to lights
//
//  fract is an 0.0 - 1.0 fraction towards the next frame
//
void morph_frame(byte c, float fract) {
  for (byte t = 0; t < NUM_BIG_TRI; t++) {
    for (int p = 0; p < NUM_PIXELS; p++) {
      morph_buffer[c][t][p] = interp_color(curr_buffer[c][t][p], next_buffer[c][t][p], fract);   
    }
  }
}

color adj_brightness(color c) {
  // Adjust only the 3rd brightness channel
  return color(hue(c), saturation(c), brightness(c) * BRIGHTNESS / 100);
}

color colorCorrect(color c) {
  short new_hue;
  
  switch(COLOR_STATE) {
    case 1:  // no red
      new_hue = map_range(hue(c), 40, 200);
      break;
    
    case 2:  // no green
      new_hue = map_range(hue(c), 120, 45);
      break;
    
    case 3:  // no blue
      new_hue = map_range(hue(c), 200, 120);
      break;
    
    case 4:  // all red
      new_hue = map_range(hue(c), 200, 40);
      break;
    
    case 5:  // all green
      new_hue = map_range(hue(c), 40, 130);
      break;
    
    case 6:  // all blue
      new_hue = map_range(hue(c), 120, 200);
      break;
    
    default:  // all colors
      new_hue = (short)hue(c);
      break;
  }
  return color(new_hue, saturation(c), brightness(c));
}

//
// map_range - map a hue (0-255) to a smaller range (start-end)
//
short map_range(float hue, int start, int end) {
  int range = (end > start) ? end - start : (end + 256 - start) % 256 ;
  return (short)((start + ((hue / 255.0) * range)) % 256);
}
  
void initializeColorBuffers() {
  for (int c = 0; c < NUM_CHANNELS; c++) {
    fill_black_one_channel(c);
  }
}

void fill_black_one_channel(int c) {
  color black = color(0,0,0); 
  for (byte t = 0; t < NUM_BIG_TRI; t++) {
    for (int p = 0; p < NUM_PIXELS; p++) {
      curr_buffer[c][t][p] = black;
      next_buffer[c][t][p] = black;
    }
  }
}

void pushColorBuffer(byte c) {
  for (byte t = 0; t < NUM_BIG_TRI; t++) {
    for (int p = 0; p < NUM_PIXELS; p++) {
      curr_buffer[c][t][p] = next_buffer[c][t][p];
    }
  }
}

void print_memory_usage() {
  long maxMemory = Runtime.getRuntime().maxMemory();
  long allocatedMemory = Runtime.getRuntime().totalMemory();
  long freeMemory = Runtime.getRuntime().freeMemory();
  int inUseMb = int(allocatedMemory / 1000000);
  
  if (inUseMb > 80) {
    println("Memory in use: " + inUseMb + "Mb");
  }  
}

color interp_color(color c1, color c2, float fract) {
 // standard lerpColor interpolation does not work well
 // for HSV colors if one color is black
 if (is_black(c1) && is_black(c2)) {
   return c1;
 } else if (is_black(c1)) {
  return color(hue(c2), saturation(c2), brightness(c2) * fract);
 } else if (is_black(c2)) {
  return color(hue(c1), saturation(c1), brightness(c1) * (1.0 - fract));
 } else {
   return color(lerp(hue(c1), hue(c2), fract),
                lerp(saturation(c1), saturation(c2), fract),
                lerp(brightness(c1), brightness(c2), fract));
 }
} 

boolean is_black(color c) {
  return (hue(c) == 0 && saturation(c) == 0 && brightness(c) == 0);
}
