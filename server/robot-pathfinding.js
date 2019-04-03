var PF = require('pathfinding')
const db = require('./db')

makeWarehouse = (width, height) => {
    // create grid
    var walkable_grid = []
    for (var i = 0; i < height; i++) {
        var to_push = []
        for (var j = 0; j < width; j++) {
            to_push.push(0)
        }
        walkable_grid.push(to_push)
    }

    var number_of_shelves = Math.floor(height / 2)

    // add shelves
    for (var s = 0; s < number_of_shelves; s++) {
        for (var i = 1; i < width - 1; i++) {
            walkable_grid[s * 2][i] = 1
        }
    }
    return walkable_grid
}

pathfind_to_point = (current_pos, end_pos, warehouse_grid) => {
    var pf_grid = new PF.Grid(warehouse_grid)
    var finder = new PF.AStarFinder()
   
    var path = finder.findPath(current_pos[0], current_pos[1], end_pos[0], end_pos[1], pf_grid)
    path = PF.Util.compressPath(path)
    
    return path
}
generate_drop_instruction = () => {
    return {
        command: 'drop'
    }
}
generate_grab_instruction = (height) => {
    return {
            command: 'grab',
            parameters: {'height':height}
        }
    x
}

generate_lift_instruction = (start, end) => {
    return {
        command: 'lift',
        parameters: {
            height: end - start
        }
    }
}
generate_movement_instruction = (start, end) => {
    if (start[1] == end[1]) {
        // we are moving in the x plane
        var num_blocks = end[0] - start[0]
        var direction = ''
        if (num_blocks < 0) {
            direction = 'forward'
            num_blocks = num_blocks * -1
        } else {
            direction = 'backward'
        }
    } else {
        var num_blocks = end[1] - start[1]
        var direction = ''
        if (num_blocks < 0) {
            direction = 'right'
            num_blocks = num_blocks * -1
        } else {
            direction = 'left'
        }
    }
    return {
        command: 'move',
        parameters: {
            blocks: num_blocks,
            direction: direction
        }
    }
}
package_items_into_groups = (item_list) => {
    var sorted_items = {"tiny":[],"small":[],"large":[]}
    for(var i = 0; i < item_list.length; i++) {
        var item = item_list[i]
        for (var j = 0; j < item['quantity']; j++) {
            sorted_items[item['size']].push(item)
        }
    }
    var item_groups = []
  
    for (var i = 0; i < sorted_items.large.length;i++) {
        item_groups.push([sorted_items.large[i]])
    }
       
    
   
    for (var i = 0; i < sorted_items.small.length; i+=2) {
        if (i + 1 < sorted_items.small.length) {
            item_groups.push([sorted_items.small[i],sorted_items.small[i+1]])
        } else {
           if (sorted_items.tiny.length >= 1) {
               item_groups.push([sorted_items.tiny.pop(),sorted_items.small[i]])
           } else {
               
               item_groups.push([sorted_items.small[i]])
           }
        }
    }
    for (var i = 0; i < sorted_items.tiny.length; i+=3) {
        to_push = [sorted_items.tiny[i]]
        if (i + 1 < sorted_items.tiny.length) {
            to_push.push(sorted_items.tiny[i+1])
        }
        if (i + 2 < sorted_items.tiny.length) {
            to_push.push(sorted_items.tiny[i+2])
        }
        item_groups.push(to_push)
    }
    return item_groups
}
 convert_order_to_job = (order, robot, warehouse_grid) => {
    if (order == undefined) {
        return {}
    }
    var robot_pos = robot['location']
    
    const item_list = order['items']
    const item_groups = package_items_into_groups(item_list)
    var job = {
        id: order['_id'],
        instruction_set: []
    }
    var robot_xy = [robot_pos['x'], robot_pos['y'], robot_pos['z']]
    const robot_home_xy = [robot['home_x'],robot['home_y']]
    // collect item groups
    console.log(item_groups)
    for (var i = 0; i < item_groups.length; i++) {
        var current_group = item_groups[i]
        var path = []
        for (var j = 0; j < current_group.length; j++) {
            var current_item = current_group[j]['position']
            var item_xy = [current_item['x'], current_item['y'], current_item['z']]
            
            path = pathfind_to_point(robot_xy, item_xy, warehouse_grid)
            if (path == [] || path == undefined) {
                return {}
            }
            //go to position and grab
            for (var p = 1; p < path.length; p++) {
                job['instruction_set'].push(generate_movement_instruction(path[p - 1], path[p]))
            }
          
              
            job['instruction_set'].push(generate_grab_instruction(item_xy[2]))
           
            robot_xy = [item_xy[0],item_xy[1],0]
        }
        // return home
        path = pathfind_to_point(robot_xy, robot_home_xy, warehouse_grid)
        for (var p = 1; p < path.length; p++) {
            job['instruction_set'].push(generate_movement_instruction(path[p - 1], path[p]))
        }
        job['instruction_set'].push(generate_drop_instruction())
        robot_xy = [robot_home_xy[0],robot_home_xy[1],0]
    }
    return job
}
module.exports.get_robot_path = (order, robot, warehouse) => {
    var warehouse_dims = warehouse['dimensions']
    var warehouse_grid = makeWarehouse(warehouse_dims['x'], warehouse_dims['y'])
    return convert_order_to_job(order, robot, warehouse_grid)
}
