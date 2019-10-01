# Intelligent Slice Plugin (USER INTERFACE)

**VERSION: 19.0.2.0**

This repository contains the **USER INTERFACE** to be used with the Intelligent Slice Plugin.  
This plugin provides an interface within Ultimaker Cura so that Teton Simulation's proprietary
smart slicing algorithms can be conveniently used by end-users without leaving the part modeling interface.

### Table of Contents
*  [Getting Started](#getting-started)
    * [Versioning](#versioning)
    * [Prerequisites](#prerequisites)
    * [Installation](#installation)
        * [Linux and UNIX](#linux-and-unix)
        * [Windows](#windows)
*   [Project Features](#project-features)
    * [Loads](#loads)


## Getting Started 

#### Versioning

Semantic versioning is employed with the following format:

`X.Y.Z.B`

*  `X` represents the MAJOR version (Denoted by last two digits of year)
*  `Y` represents the MINOR version
*  `Z` represents the REVISION version
*  `B` represents the BUILD version

#### Prerequisites

*  Ultimaker Cura

#### Installation

###### Linux and UNIX

```bash
[user@computer ~]$ cd .local/share/cura/[VERSION NUMBER]/plugins/
[user@computer plugins] git clone https://github.com/tetonsim/is-cura-ui.git
```

###### Windows

*Commentary needed by Windows User*


##  Project Features

*  Basic Interface Features
    *  Provides new tab labeled "SMART SLICE" to on right side of standard top bar options (e.g. PREPARE, PREVIEW, MONITOR)
*  Smart Slice Button
    *  When Smart Slice environment is entered, the 'Slice' button is replaced by a 'Smart Slice' button
    *  The Smart Slice button becomes active when the following minimum requirements are met: One **Anchor** and One **Load**
*  Use Case Dialogue
    *  The **Use Case** Dialogue allows a user to specify the desired boundary conditions for a part
    *  A 'Use Case' can consist of one or many anchors and loads
    *  *Currently*, only one 'Use Case' can be applied to a part
*  Requirements Dialogue
    *  Upon selecting a part, an end-user can apply requirements to a part to ensure a criterea is met
    *  Current selectable requirements include: **Maximum Displacement** and **Safety Factor**
*  AWS Job Integration
    *  End-users can submit/cancel optmization/validation jobs with AWS services
    *  AWS returns a report that either validates the job or explains existing problems
    *  A validated part might then be further optimized (assuming it is not then over-fitted)

####  Loads

A load can be a Pushing or Pulling kinetic force.  Users apply these loads by selecting a surface, while in 'Smart Slice' mode,  and modifying the values on the new dialogue within the canvas.  Loads can be further refined by right-clicking a surface and selecting *edit load*.  The load is represented by an arrow pointing in the normal direction of the force.  


