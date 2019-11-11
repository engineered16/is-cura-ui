/*
  NormalArrow.qml
  Teton Simulation
  Authored on   November 11, 2019
  Last Modified November 11, 2019
*/

/*
  Contains definition for SmartSlice Normal Vector Arrow
*/


//  3D Library Imports 
import Qt3D.Core 2.0
import Qt3D.Render 2.0


Item {
    id: "SmartSliceNormalArrow"


    /*
      material:
        Default unlit mesh material
    */
    PhongMaterial {
        id: NormalArrowMaterial
    }


    /*
      ARROW SHAFT:
        Geometrical definition for shaft of normal vector arrow  
        NOTE: 'radius' and 'length' should probably be derived using model mesh size
    */
    CylinderMesh {
        id: ArrowShaftMesh

        radius: 3  //  Arbitrary Testing Numbers
        length: 10

        rings: 100
        slices: 20
    }

    //  Arrow Shaft Placement
    Transform {
        id: ArrowShaftTransform

        //  x, y, z  Coordinates; Derived from selected surface location
        property real x_coord: 0
        property real y_coord: 0
        property real z_coord: 0

        //  Euler Angles for Rotation; Derived from selected surface's normal vector
        property real x_rot: 0
        property real y_rot: 0
        property real z_rot: 0

        //  Build Transform Matrix for ArrowShaft
        matrix: {
            var m = Qt.matrix4x4();
            m.rotate(0.0, x_rot, y_rot, z_rot)
            m.translate(Qt.vector3d(x_coord, y_coord, z_coord));
            return m;
        }
    }

    //  Arrow Shaft Entity
    Entity {
        id: ArrowShaftEntity
        components: [ArrowShaftMesh, NormalArrowMaterial, ArrowShaftTransform]
    }


    /*
      ARROW HEAD:
        NOTE: 'radius' and 'length' should probably be derived using model mesh size
    */
    ConeMesh {
        id: ArrowHeadMesh

        //  Set Arrow Head Size
        bottomRadius: 5
        topRadius: 0
        length: 3

        rings: 25
        slices: 5
    }

    //  Arrow Head Placement
    Transform {
        id: ArrowHeadTransform

        //  x, y, z  Coordinates; Derived from selected surface location
        property real x_coord: 0// + (10*x_norm)
        property real y_coord: 0// + (10*y_norm)
        property real z_coord: 0// + (10*z_norm)

        //  Euler Angles for Rotation; Derived from selected surface's normal vector
        property real x_rot: 0
        property real y_rot: 0
        property real z_rot: 0

        //  Normal Vector Components
        property real x_norm: 0
        property real y_norm: 0
        property real z_norm: 0

        //  Build Transform Matrix for ArrowShaft
        matrix: {
            var m = Qt.matrix4x4();
            m.rotate(0.0, x_rot, y_rot, z_rot)
            m.translate(Qt.vector3d(x_coord+(10*x_norm), y_coord+(10*y_norm), z_coord+(10*z_norm)));
            return m;
        }
    }

    //  Arrow Head Entity
    Entity {
        id: ArrowHeadEntity
        components: [ArrowHeadMesh, NormalArrowMaterial, ArrowHeadTransform]
    }
}



