const sender = function sender(x) {
    function add(x) {
        function times(x) {
            return x * x
        }
        return x + times(x)
    }
    return add(x)
}


const times = function times(x) {
    return x * x
}

const add = function add(x) {
    return x + x
}

const wrapper = function wrapper(add, times) {
    return function(add) {
        return function(times) {
            return times(x)
        }
    }
}

function makeAdder(x) {
    return function(y) {
      return (x + 1) * y;
    };
  }

  var add5 = makeAdder(5);
  var add10 = makeAdder(10);

  console.log(add5(2));  // 7
  console.log(add10(2)); // 12

// console.log('------------------------------------');
// console.log(add(times(2)));
// console.log('------------------------------------');
// console.log('------------------------------------');
// console.log(wrapper(2));
// console.log('------------------------------------');


// function add(x) {
//     function times(x) {
//         return x * x
//     }
//     return x + times(x)
// }
// console.log('------------------------------------');
// console.log(add(2));
// console.log('------------------------------------');
// console.log('------------------------------------');
// console.log(sender(2));
// console.log('------------------------------------');
// console.log('------------------------------------');
// console.log(sender(2) === add(times(2)));
// console.log('------------------------------------');
