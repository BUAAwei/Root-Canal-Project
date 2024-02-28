<template>
  <div id="three-container"></div>
</template>
  
  <script>
import * as THREE from "three";
import { STLLoader } from "three/examples/jsm/loaders/STLLoader";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls";
import * as dat from "dat.gui";
let cuttingPlane = null;
let mouse = new THREE.Vector2();
let raycaster = new THREE.Raycaster();
let scene = null;
let camera = null;
export default {
  mounted() {
    this.initThreeJS();
    setTimeout(() => {
      window.addEventListener('mousemove', this.onMouseMove);
    }, 5000);
  },
  methods: {
    initThreeJS() {
      scene = new THREE.Scene();
      // 设置正交相机参数
      camera = new THREE.PerspectiveCamera(
        75,
        window.innerWidth / window.innerHeight,
        0.1,
        1000
      );

      camera.position.z = 300;
      camera.position.x = 500;
      camera.position.y = 500;
      camera.rotation.z = 100;

      // rotate the camera

      const renderer = new THREE.WebGLRenderer();
      renderer.setSize(600, 400);
      document
        .getElementById("three-container")
        .appendChild(renderer.domElement);

      const ambientLight = new THREE.AmbientLight(0x404040);
      scene.add(ambientLight);

      const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
      directionalLight.position.set(1, 1, 1);
      scene.add(directionalLight);

      // STL 文件加载
      const loader = new STLLoader();
      loader.load("/models/output.stl", (geometry) => {
        geometry.computeVertexNormals(); // 计算顶点法线以平滑化

        const material = new THREE.MeshNormalMaterial();
        const mesh = new THREE.Mesh(geometry, material);
        scene.add(mesh);

        // mesh.position.set(0,0,0);
        // // 计算模型的边界框并居中
        // const boundingBox = new THREE.Box3().setFromObject(mesh);
        // const center = boundingBox.getCenter(new THREE.Vector3());
        // mesh.position.x += mesh.position.x - center.x;
        // mesh.position.y += mesh.position.y - center.y;
        // mesh.position.z += mesh.position.z - center.z;

        // 更新摄像机位置
        //   camera.lookAt(center);
      });


      loader.load("/models/output.stl", (geometry) => {
        geometry.computeBoundingBox(); // 计算模型的边界框
        const boundingBox = geometry.boundingBox;
        const sliceCount = 300; // 切片数量


        const points = [];
        // 计算每个切片的高度和质心
        for (let i = 0; i < sliceCount; i++) {
          const z = boundingBox.min.z + i * (boundingBox.max.z - boundingBox.min.z) / (sliceCount - 1);
          const z2 = boundingBox.min.z + (i+1) * (boundingBox.max.z - boundingBox.min.z) / (sliceCount - 1);
          const sliceGeometry = new THREE.BufferGeometry();

            const sliceVertices = [];
            const position = geometry.attributes.position;

            // 筛选顶点位置
            for (let j = 0; j < position.count; j += 3) {
            const vertexZ = position.getZ(j);
            if (vertexZ >= z && vertexZ < z2) {
                const vertexX = position.getX(j);
                const vertexY = position.getY(j);
                sliceVertices.push(new THREE.Vector3(vertexX, vertexY, vertexZ));
            }
            }


          if (sliceVertices.length > 0){
            const centerOfMass = new THREE.Vector3();
            sliceVertices.forEach(vertex => centerOfMass.add(vertex));
            centerOfMass.divideScalar(sliceVertices.length);

            // 绘制质心
            points.push(centerOfMass);
            // const dotGeometry = new THREE.BufferGeometry();
            // dotGeometry.vertices.push(centerOfMass);
            // const dotMaterial = new THREE.PointsMaterial({ color: 0xff0000, size: 5 });
            // const dot = new THREE.Points(dotGeometry, dotMaterial);
            // scene.add(dot);

            // console.log(i + dot)
          }
          // 计算质心
          
        }
        console.log(points);
        // 创建 CatmullRomCurve3 曲线
        // const curve = new THREE.CatmullRomCurve3(points,undefined, 'catmullrom', 1.0);

        const curve = new THREE.CubicBezierCurve3(points);
        console.log(curve);
        // 获取曲线上的点
        // const smoothPoints = curve.getPoints(100); // 获取 100 个平滑点
        // const ggeometry = new THREE.BufferGeometry().setFromPoints( curve );
        // 从曲线对象中获取平滑点
        const smoothPoints = curve.getPoints(10);

        
        // 创建 BufferGeometry 对象并设置点集
        const ggeometry = new THREE.BufferGeometry().setFromPoints(smoothPoints);

        // 使用 BufferGeometry 创建线条对象
        const lline = new THREE.Line(ggeometry, material);

        // 将线条添加到场景中
        scene.add(lline);

      });

      //create a blue LineBasicMaterial
    const material = new THREE.LineBasicMaterial( { color: 0x00ff00  } );
    const points = [];
    points.push( new THREE.Vector3( - 100, 0, 0 ) );
    points.push( new THREE.Vector3( 0, 100, 0 ) );
    points.push( new THREE.Vector3( 100, 0, 0 ) );
    


    const geometry = new THREE.BufferGeometry().setFromPoints( points );
    const line = new THREE.Line( geometry, material );
    scene.add( line );

      // 创建切平面但暂时不加入到场景中
      const planeGeometry = new THREE.PlaneGeometry(20, 20);
      const planeMaterial = new THREE.MeshPhongMaterial({ color: 0x00ff00 });
      cuttingPlane = new THREE.Mesh(planeGeometry, planeMaterial);
      cuttingPlane.visible = true; // 初始状态不可见
      scene.add(cuttingPlane);

      const controls = new OrbitControls(camera, renderer.domElement);
      controls.addEventListener('change', () => renderer.render(scene, camera));

      // 使用dat.gui添加控制器
      const gui = new dat.GUI();
      const cameraFolder = gui.addFolder("Camera");
      const cameraPositionController = cameraFolder.addFolder("Position");
      cameraPositionController.add(camera.position, "x", -1000, 1000).name("X");
      cameraPositionController.add(camera.position, "y", -1000, 1000).name("Y");
      cameraPositionController.add(camera.position, "z", -1000, 1000).name("Z");
      const cameraRotationController = cameraFolder.addFolder("Rotation");
      cameraRotationController
        .add(camera.rotation, "x", -Math.PI, Math.PI)
        .name("X");
      cameraRotationController
        .add(camera.rotation, "y", -Math.PI, Math.PI)
        .name("Y");
      cameraRotationController
        .add(camera.rotation, "z", -Math.PI, Math.PI)
        .name("Z");
      cameraFolder.open();


      
      const animate = () => {
        requestAnimationFrame(animate);
        renderer.render(scene, camera);
      };

      animate();
    },

    onMouseMove(event) {
      mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
      mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;

      raycaster.setFromCamera(mouse, camera);
      const intersects = raycaster.intersectObjects(scene.children);
    //   if (intersects.length > 0) {
    //     // 使切平面与交点对齐
    //     console.log("Collision");
    //     const intersect = intersects[0];
    //     cuttingPlane.position.copy(intersect.point);

    //     // 切平面与相交点的法线方向对齐
    //     // cuttingPlane.lookAt(intersect.point.clone().add(intersect.face.normal));

    //     // cuttingPlane.visible = true;
    //   } else {
    //     console.log("Not Collision");
    //     cuttingPlane.visible = false; // 当不与模型相交时不显示
    //     // set the cuttingplan unvisable
    //     // what do you mean
    //   }
    },
  },
};
</script>
  
  <style scoped>
#three-container {
  width: 400px; /* 设置宽度为400px */
  height: 300px; /* 设置高度为300px */
}
</style>
  