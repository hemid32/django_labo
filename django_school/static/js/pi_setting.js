
// cett function pour  test file  loading
function h(){
            var stl_red ="stroke:rgb(255,0,0);stroke-width:2";
            document.getElementById("resistance").setAttribute("style",stl_red);

            }

/*
var Gpio = require('onoff').Gpio; //include onoff to interact with the GPIO
var s1 = new Gpio(4, 'out');
var s2 = new Gpio(5, 'out');
var s3 = new Gpio(6, 'out');
var s4 = new Gpio(7, 'out');
var s5 = new Gpio(8, 'out');
var s6 = new Gpio(9, 'out');

function RC_val(v,v1) { //function to start blinking
  //if (s1.readSync() === 0) { //check the pin state, if the state is 0 (or off)
  //  LED.writeSync(1); //set pin state to 1 (turn LED on)
  //} else {
  //  LED.writeSync(0); //set pin state to 0 (turn LED off)
  //h();
  // s1 == r1 s2== r2  s3==c1 s4 ==c2 s5 == c3 s6 == osillo
  var r1 == 10 ;
  var r2 == 50 ;
  var c1 == 10 ;
  var c2 == 30 ;
  var c3 == 50 ;
  disable_gpio();
  if(v == r1){
    s1.writeSync(1); //set pin state to 1 (turn switch on)
    }
  if(v == r2){
    s2.writeSync(1); //set pin state to 1 (turn switch on)
    }
  if(v == ((r1*r2)/(r1+r2)).toFixed(2)){
    s1.writeSync(1); //set pin state to 1 (turn switch on)
    s2.writeSync(1); //set pin state to 1 (turn switch on)
    }
  if(v1 == c1){
    s3.writeSync(1); //set pin state to 1 (turn switch on)
    }
  if(v1 == c2){
    s4.writeSync(1); //set pin state to 1 (turn switch on)
    }
  if(v1 == c3){
    s5.writeSync(1); //set pin state to 1 (turn switch on)
    }
  if(v1 == c1+c2){
    s3.writeSync(1); //set pin state to 1 (turn switch on)
    s4.writeSync(1); //set pin state to 1 (turn switch on)
  if(v1 == c1+c3){
    s3.writeSync(1); //set pin state to 1 (turn switch on)
    s5.writeSync(1); //set pin state to 1 (turn switch on)
    }
  if(v1 == c2+c3){
    s4.writeSync(1); //set pin state to 1 (turn switch on)
    s5.writeSync(1); //set pin state to 1 (turn switch on)
    }
  if(v1 == c1+c2+c3){
    s3.writeSync(1); //set pin state to 1 (turn switch on)
    s4.writeSync(1); //set pin state to 1 (turn switch on)
    s5.writeSync(1); //set pin state to 1 (turn switch on)
    }

   s6.writeSync(1); //set pin state to 1 (turn osilo on)

  }
function disable_gpio(){
    s1.writeSync(0); //set pin state to 0 (turn LED off)
    s2.writeSync(0); //set pin state to 0 (turn LED off)
    s3.writeSync(0); //set pin state to 0 (turn LED off)
    s4.writeSync(0); //set pin state to 0 (turn LED off)
    s5.writeSync(0); //set pin state to 0 (turn LED off)
    s6.writeSync(0); //set pin state to 0 (turn LED off)
}
*/
