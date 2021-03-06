let rSlider


let dt = 0.005;
let t = 0;

let canvas_width = 1000;
let canvas_height = 600;

let x_center = canvas_width / 2;

let L_span = 50;
let base_height = 150;

let x_scaling_factor = L_span / 200;
let y_scaling_factor = base_height / 500;

let draw_scale = 3;

let cp = [
  [x_center - L_span, base_height],
  [x_center - L_span - 80.5*x_scaling_factor, base_height],
  [x_center - L_span - 100*x_scaling_factor, base_height - 138.9*y_scaling_factor],
  [x_center - L_span - 100*x_scaling_factor, base_height - 138.9*y_scaling_factor],
  [x_center - L_span - 100*x_scaling_factor, base_height - 138.9*y_scaling_factor],
  [x_center, base_height - 138.9*y_scaling_factor],
  [x_center, base_height - 138.9*y_scaling_factor],
  [x_center, base_height - 178.6*y_scaling_factor],
  [x_center + L_span + 103.2*x_scaling_factor, base_height - 178.6*y_scaling_factor],
  [x_center + L_span + 103.2*x_scaling_factor, base_height - 178.6*y_scaling_factor],
  [x_center + L_span + 82.6*x_scaling_factor, base_height],
  [x_center + L_span, base_height],
];

let path_history = [];

function setup() {
  createCanvas(canvas_width, canvas_height);
  for(var i = 0; i < cp.length; i++) {
    cp[i] = [(cp[i][0] - x_center) * draw_scale + x_center, cp[i][1] * draw_scale]
  }
}

function recursive_bezier(points) {
  let path_flag = false;
  if (points.length > 1) {
    let distances = [];
    let new_points = [];
    for (var i = 0; i < points.length; i++) {
      if (i < points.length - 1) {
        distances.push([points[i+1][0] - points[i][0], points[i+1][1] - points[i][1]]);
      }
    }
    for (var i = 0; i < points.length-1; i++) {
      strokeWeight(1);
      stroke('black');
      let curr_point = points[i];
      let next_point = points[i+1];
      line(curr_point[0], curr_point[1], next_point[0], next_point[1]);

      strokeWeight(10);
      stroke('gray');
      if(points.length == 2) {
        stroke('red');
        path_flag = true;
      }
      point(curr_point[0] + distances[i][0]*t, curr_point[1] + distances[i][1]*t);
      new_points.push([curr_point[0] + distances[i][0]*t, curr_point[1] + distances[i][1]*t]);
      if(path_flag) {
        path_history.push([curr_point[0] + distances[i][0]*t, curr_point[1] + distances[i][1]*t]);
      }
    }

    recursive_bezier(new_points);
  }
}

function draw() {
  background('#E0E0E0');
  strokeWeight(5);
  stroke('#8a8a8a');
  line(0,2.5,canvas_width,2.5);
  line(canvas_width / 2, 0, canvas_width / 2, canvas_height);
  strokeWeight(20);
  stroke('black');
  point(x_center, 0);

  recursive_bezier(cp);

  strokeWeight(3);
  stroke('red');
  for (var i = 0; i < path_history.length-1; i++) {
    line(path_history[i][0], path_history[i][1], path_history[i+1][0], path_history[i+1][1]);
  }

  for (var i = 0; i < cp.length; i++) {
    strokeWeight(10);
    stroke('#55acee');
    if(i == 0 || i == cp.length - 1){
      stroke('#1e679e');
    }
    point(cp[i][0], cp[i][1]);
  }

  t += dt; // t is the spline parameter, not neceessarily time.
  if (t > 1) {
    t = 0;
    path_history = [];
  }
}
