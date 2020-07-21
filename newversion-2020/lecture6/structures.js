let name1 = "Bilge";
let surname = "Demir";

const fullName = `${surname} 
${name1}`                           // just go next line if you want outputs to be next line

console.log(fullName);



// Destructuring objects 

const player = {
    name:'Lebron James',
    club:'LA Lakers',
    adress: {
        city:'Los Angeles',
        neighbour:'Santa Monica',
    }
};

console.log(player.name);  /// Lebron James
console.log(player.city); /// undefined

console.log(player.adress.neighbour);  /// Santa Monica
// but you can do that in a better way :

const {name, club} = player;


// now you can do:

console.log(`${name} is playing for ${club}`); // we broke down player.name structure

// to do it for city for example:

const {adress: {city, neighbour}} = player;
console.log(`${neighbour} is the neighbor of the ${city}`);


/// Destructuring Arrays

let names = ['Bilge','Asli','Minnos']; /// we can create a pointer element to destructure

console.log(names[1]) // normally we do that but lets create a pointer:

let [person1] = ['Bilge','Asli','Minnos']

console.log(person1) /// Bilge

let [personx,persony,person3] = ['Bilge','Asli','Minnos']

console.log( personx, persony)  /// Bilge Asli
console.log(person3)  /// Minnos


// we can override the value

person3 = 'noMinnos'

console.log(person3)  /// noMinnos



