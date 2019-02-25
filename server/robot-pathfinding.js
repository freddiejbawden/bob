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
            walkable_grid[s * 2 + 1][i] = 1
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
generate_grab_instruction = () => {
    return {
        command: 'grab'
    }
}

generate_lift_instruction = (start, end) => {
    return {
        command: 'lift',
        parameters: {
            height: Math.abs(start - end)
        }
    }
}
generate_movement_instruction = (start, end) => {
    if (start[1] == end[1]) {
        // we are moving in the x plane
        var num_blocks = end[0] - start[0]
        var direction = ''
        if (num_blocks < 0) {
            direction = 'left'
            num_blocks = num_blocks * -1
        } else {
            direction = 'right'
        }
    } else {
        var num_blocks = end[1] - start[1]
        var direction = ''
        if (num_blocks < 0) {
            direction = 'backwards'
            num_blocks = num_blocks * -1
        } else {
            direction = 'forwards'
        }
    }
    return {
        command: 'move',
        parameter: {
            blocks: num_blocks,
            direction: direction
        }
    }
}
convert_order_to_job = (order, robot, warehouse_grid) => {
    if (order == undefined) {
        return {}
    }
    var robot_pos = robot['location']
    var item_list = order['items']

    var job = {
        id: order['_id'],
        instruction_set: []
    }
    var robot_xy = [robot_pos['x'], robot_pos['y'], robot_pos['z']]
    for (var i = 0; i < item_list.length; i++) {
        var current_item = item_list[i]['position']
        var item_xy = [current_item['x'], current_item['y'] * 2, robot_pos['z']]

        var path = pathfind_to_point(robot_xy, item_xy, warehouse_grid)
        if (path == [] || path == undefined) {
            return {}
        }
        //go to position and grab
        for (var p = 1; p < path.length; p++) {
            job['instruction_set'].push(generate_movement_instruction(path[p - 1], path[p]))
        }
        if (robot_xy[2] != item_xy[2]) {
            job['instruction_set'].push(generate_lift_instruction(robot_xy[2], item_xy[2]))
        }
        job['instruction_set'].push(generate_grab_instruction())
        // return home
        for (var p = path.length - 1; p > 0; p--) {
            job['instruction_set'].push(generate_movement_instruction(path[p], path[p - 1]))
        }
        job['instruction_set'].push(generate_drop_instruction())
    }

    return job
}
module.exports.get_robot_path = (order, robot, warehouse) => {
    var warehouse_dims = warehouse['dimensions']
    var warehouse_grid = makeWarehouse(warehouse_dims['x'], warehouse_dims['y'])
    return convert_order_to_job(order, robot, warehouse_grid)
}
