function generate_state(row,column) {
  return "square_"+row+"_"+column
}
function generate_link(row1,col1,row2,col2) {
  var sq_1 = generate_state(row1,col1)
  var sq_2 = generate_state(row2,col2)

  return "(nextto " + sq_1 + " " + sq_2 + ")"

}
function parseLayout(){
  var fs = require('fs')
  filename = './warehouse-layout.csv'
  fs.readFile(filename, 'utf8', function(err, data) {
    if (err) throw err;
    console.log('OK: ' + filename);
    console.log('Generating file for plan')
    var clauses = data.split('\n')

    var warehouse_layout = [];
    for (var i = 0; i < clauses.length-1; i++) {
      warehouse_layout[i] = clauses[i].replace('\r','').split(',')
    }

    var states = []
    for (var row = 0; row < warehouse_layout.length; row++) {

      for (var col = 0; col <warehouse_layout[row].length;col++){
        if (warehouse_layout[row][col] > 0) {
          if (row > 0) {
            if (warehouse_layout[row-1][col] > 0) {
              states.push(generate_link(row,col,row-1,col))
            }
          }
          if (row < warehouse_layout.length - 1) {
            if (warehouse_layout[row+1][col] > 0) {
              states.push(generate_link(row,col,row+1,col))
            }
          }
          if (col > 0) {
            if (warehouse_layout[row][col-1] > 0) {
              states.push(generate_link(row,col,row,col-1))
            }
          }
          if (col < warehouse_layout[row].length - 1) {
            if (warehouse_layout[row][col+1] > 0) {
              states.push(generate_link(row,col,row,col+1))
            }
          }
          if (warehouse_layout[row][col] == 2) {
            states.push("(at robot" + generate_state(row,col));
          }
        }
      }
    }
    createWorldJSON(states)
  });
}
function createWorldJSON(states) {
  var world_state = {};
  world_state['states'] = states;
  world_json = JSON.stringify(states);
  exports.world_json = world_json;
}
parseLayout();
