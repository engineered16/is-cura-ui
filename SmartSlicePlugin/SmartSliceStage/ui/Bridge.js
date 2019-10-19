/*
    bridge.js
    Teton Simulation
    Authored on   October 16, 2019
    Last Modified October 16, 2019
*/

/*
    Contains Interface functionality for communicating between UM/Cura server and QML

    
    TABLE OF CONTENTS
    =================
    1.) REQUIREMENTS
        1.a) Safety Factor
        1.b) Maximum Deflection
    2.) TIME ESTIMATION
        2.a) Infills
        2.b) Inner Walls
        2.c) Outer Walls
        2.d) Retractions
        2.e) Skin
        2.f) Skirt
        2.g) Travel
    3.) MATERIAL ESTIMATION
        3.a) Material
        3.b) Length
        3.c) Weight
        2.d) Cost
*/


//  1.) REQUIREMENTS
/*
    1.a) Safety Factor
*/
function SafetyFactorComputed()
{
    var sfc = _bridge._SafetyFactorComputed();

    return sfc
}

function SafetyFactorTarget()
{
    return "> " + "4"
}


/*
    1.b) Maximum Deflection
*/
function MaxDeflectionComputed()
{
    return 5 + " mm"
}

function MaxDeflectionTarget()
{
    return "> " + "2" + "mm"
}


//  2.) TIME ESTIMATION
/*
    2.a) Infills
*/
function InfillsComputed()
{
    return "04:55"
}

function InfillsTarget()
{
    return 29 + "%"
}


/*
    2.b) Inner Walls
*/
function InnerWallsComputed()
{
    return "06:16"
}

function InnerWallsTarget()
{
    return 38 + "%"
}


/*
    2.c) Outer Walls
*/
function OuterWallsComputed()
{
    return "01:39"
}

function OuterWallsTarget()
{
    return 10 + "%"
}


/*
    2.d) Retractions
*/
function RetractionsComputed()
{
    return "00:00"
}

function RetractionsTarget()
{
    return 0 + "%"
}


/* 
    2.e) Skin
*/
function SkinComputed()
{
    return "03:21"
}

function SkinTarget()
{
    return 20 + "%"
}


/*
    2.f) Skirt
*/
function SkirtComputed()
{
    return "00:07"
}

function SkirtTarget()
{
    return 1 + "%"
}


/* 
    2.g) Travel
*/
function TravelComputed()
{
    return "00:21"
}

function TravelTarget()
{
    return 2 + "%"
}



//  3.) MATERIAL ESTIMATION
/*
    3.a) Material
*/
function Material()
{
    return "Blue ABS"
}


/*
    3.b) Length
*/
function Length()
{
    return 18.05 + "m"
}


/*
    3.c) Weight
*/
function Weight()
{
    return 127 + "g"
}


/*
    3.d) Cost
*/
function Cost()
{
    return "$" + 32.77
}

