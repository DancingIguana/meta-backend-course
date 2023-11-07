/* OPTION 1
let answer = prompt("What is your name?");
if(typeof(answer) == "string") {
    let h1 = document.createElement("h1");
    h1.innerText = answer;
    document.body.innerText = "";
    document.body.appendChild(h1);
}
*/

/* OPTION 2 (BETTER) */
let h1 = document.createElement("h1");
h1.innerText = "Type into the input to make this text change";
let input = document.createElement("input");
input.setAttribute("type","text");

document.body.innerText = "";
document.body.appendChild(h1);
document.body.appendChild(input);

input.addEventListener('change', function() {
    h1.innerText = input.value;
});