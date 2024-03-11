<template>
  <div class="Container" style="display: flex">
    <div id="three-container"></div>
    <div id="dat-gui-container"></div>
  </div>
</template>

<script>
import * as THREE from "three";
import { STLLoader } from "three/examples/jsm/loaders/STLLoader";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls";
import * as dat from "dat.gui";
let mouse = new THREE.Vector2();
let raycaster = new THREE.Raycaster();
let scene = new THREE.Scene();
let camera = new THREE.PerspectiveCamera(
  75,
  window.innerWidth / window.innerHeight,
  0.1,
  10000
);

let centX = 0;
let centY = 0;
let centZ = 0;
export default {
  mounted() {
    this.initThreeJS();
    setTimeout(() => {
      window.addEventListener("mousemove", this.onMouseMove);
    }, 5000);
  },
  methods: {
    initThreeJS() {
      camera.position.z = 300;
      camera.position.x = 500;
      camera.position.y = 500;
      camera.rotation.z = 100;

      const renderer = new THREE.WebGLRenderer();
      renderer.setSize(1400, 800);
      document
        .getElementById("three-container")
        .appendChild(renderer.domElement);

      const ambientLight = new THREE.AmbientLight(0x404040);
      scene.add(ambientLight);

      const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
      directionalLight.position.set(1, 1, 1);
      scene.add(directionalLight);

      const loader = new STLLoader();

      var centerDistance = new THREE.Vector3();
      loader.load("/models/output1.stl", (geometry) => {
        geometry.computeVertexNormals();
        geometry.computeBoundingBox();

        const boundingBox = new THREE.Box3();
        boundingBox.setFromObject(new THREE.Mesh(geometry));
        // center = new THREE.Vector3();

        boundingBox.getCenter(centerDistance);

        console.log("Geometry centerDistance:", centerDistance);
        centX = centerDistance.x;
        centY = centerDistance.y;
        centZ = centerDistance.z;
        console.log(
          "centX" + centX + "centY" + centY + "centZ" + centZ + "..."
        );

        // console.log(boundingBox);
        // make the geometry to the centerDistance of the scene
        // get the geometry's offset to the centerDistance of the scene
        // centerDistanceDistance = geometry.boundingSphere.center.length();
        geometry.center();

        // create a transparent but clear used in medical imaging material
        //   const material = new THREE.MeshStandardMaterial({
        // 	// color: 0x00ff00,
        // 	// transparent: true,
        // 	opacity: 0.2,
        // 	metalness: 0.1,
        // 	roughness: 0.9,
        //   });

        // create a transparent but clear used in medical imaging material
        const material = new THREE.MeshStandardMaterial({
          opacity: 0.6,
          transparent: true,
          metalness: 0.3,
          roughness: 1.2,
        });
        const mesh = new THREE.Mesh(geometry, material);
        scene.add(mesh);

        const fileloader = new THREE.FileLoader();
        const swcPath = "/models/my_skeleton.swc"; // 替换为您的SWC文件路径
        console.log(centerDistance + "!!!!!!!!!!!?");
        fileloader.load(swcPath, (swcData) => {
          const lines = swcData.split("\n");

          const points = [];
          lines.forEach((line) => {
            const data = line.trim().split(" ");
            if (data.length === 7) {
              var x = parseFloat(data[2]);
              var y = parseFloat(data[3]);
              var z = parseFloat(data[4]);
              console.log(
                "centX" + centX + "centY" + centY + "centZ" + centZ + "..."
              );

              // make x y z - centerDistance
              x -= centX;
              y -= centY;
              z -= centZ;
              console.log(x + "...");
              // const radius = parseFloat(data[5]);
              const parent = parseInt(data[6]);

              // const geometry = new THREE.SphereGeometry(6, 32, 32);
              // const material = new THREE.MeshBasicMaterial({ color: 0xff0000 });
              // const sphere = new THREE.Mesh(geometry, material);
              // sphere.position.set(x, y, z);
              // scene.add(sphere);

              points.push({
                position: new THREE.Vector3(x, y, z),
                parentIndex: parent,
              });
            }
          });
          console.log(points);

          // 过滤掉包含NaN值的点
          const filteredPoints = points.filter(
            (point) =>
              !isNaN(point.position.x) &&
              !isNaN(point.position.y) &&
              !isNaN(point.position.z)
          );

          // 根据z坐标对过滤后的点进行排序
          filteredPoints.sort((a, b) => a.position.z - b.position.z);

          const zVarianceThreshold = 5; // 设定z坐标变化的最小阈值，根据你的需求调整

          const reducedPoints = filteredPoints.reduce(
            (acc, point, index, array) => {
              // 如果是最后一个点，直接添加
              if (index === array.length - 1) {
                acc.push(point);
              } else {
                // 比较当前点和下一个点的z坐标差
                const nextPoint = array[index + 1];
                const zDifference = Math.abs(
                  point.position.z - nextPoint.position.z
                );
                const xDifference = Math.abs(
                  point.position.x - nextPoint.position.x
                );
                const yDifference = Math.abs(
                  point.position.y - nextPoint.position.y
                );

                // 如果z坐标差大于等于阈值，保留这个点
                if (zDifference >= zVarianceThreshold) {
                  acc.push(point);
                }else{
                  if (xDifference >= 20 || yDifference >= 20) {
                    acc.push(point);
                  }
                }
              }
              return acc;
            },
            []
          );

          // 现在 reducedPoints 包含了去除了连续变化小的点后的数组
          // 可以继续使用 reducedPoints 进行曲线绘制等后续操作

          // 使用排序后的点创建THREE.CatmullRomCurve3实例
          console.log(reducedPoints);
          const curvePoints = reducedPoints.map(
            (point) =>
              new THREE.Vector3(
                point.position.x,
                point.position.y,
                point.position.z
              )
          );
          const curve = new THREE.CatmullRomCurve3(curvePoints);

          // 使用曲线对象生成一组平滑的点（例如，生成50个点）
          const smoothPoints = curve.getPoints(50);

          // 使用这些点创建一条线来可视化曲线
          // const lineGeometry = new THREE.BufferGeometry().setFromPoints(
          //   smoothPoints
          // );
          // const lineMaterial = new THREE.LineBasicMaterial({ color: 0xff0000, linewidth: 20 }); // 尝试增加linewidth值

          // const line = new THREE.Line(lineGeometry, lineMaterial);

          // // 将线添加到场景中
          // scene.add(line);
          // 使用曲线对象和指定的半径创建TubeGeometry
          const tubeGeometry = new THREE.TubeGeometry(curve, 20, 2, 8, false);

          // 创建材料
          const tubeMaterial = new THREE.MeshBasicMaterial({ color: 0xff0000 });

          // 创建mesh并添加到场景
          const tube = new THREE.Mesh(tubeGeometry, tubeMaterial);
          scene.add(tube);
        });
        // 让场景不要太暗，加入环境光，并且加入一些网格元素方便观察
        const aambientLight = new THREE.AmbientLight(0x804040);
        scene.add(aambientLight);
        const ddirectionalLight = new THREE.DirectionalLight(0xffffff, 6);
        ddirectionalLight.position.set(1, 1, 1);
        scene.add(directionalLight);
        // const gridHelper = new THREE.GridHelper(200, 50);
        // scene.add(gridHelper);
        // const axesHelper = new THREE.AxesHelper(100);
        // scene.add(axesHelper);
        // make a very big grid helpler and axesHelper
        const gridHelper = new THREE.GridHelper(5000, 300);
        scene.add(gridHelper);
        const axesHelper = new THREE.AxesHelper(100);
        scene.add(axesHelper);

        const controls = new OrbitControls(camera, renderer.domElement);
        controls.addEventListener("change", () =>
          renderer.render(scene, camera)
        );

        const gui = new dat.GUI();
        // make gui element in parent dat-gui-container
        // gui.domElement.id = "dat-gui-container";
        document
          .getElementById("dat-gui-container")
          .appendChild(gui.domElement);

        const cameraFolder = gui.addFolder("Camera");
        const cameraPositionController = cameraFolder.addFolder("Position");
        cameraPositionController
          .add(camera.position, "x", -1000, 1000)
          .name("X");
        cameraPositionController
          .add(camera.position, "y", -1000, 1000)
          .name("Y");
        cameraPositionController
          .add(camera.position, "z", -1000, 1000)
          .name("Z");
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

        // const cuttingPlaneFolder = gui.addFolder("Cutting Plane");
        // cuttingPlaneFolder.add(cuttingPlane.position, "x", -100, 100).name("X");
        // cuttingPlaneFolder.add(cuttingPlane.position, "y", -100, 100).name("Y");
        // cuttingPlaneFolder.add(cuttingPlane.position, "z", -100, 100).name("Z");
        // cuttingPlaneFolder.open();

        // make the points to the centerDistance

        // points.forEach((point, index) => {
        // 	if (point.parentIndex !== -1 && points[point.parentIndex] !== NaN) {
        // 		const start = point.position;
        // 		const end = points[point.parentIndex].position;

        // 		const material = new THREE.LineBasicMaterial({ color: 0x0000ff });
        // 		const geometry = new THREE.BufferGeometry().setFromPoints([start, end]);
        // 		const line = new THREE.Line(geometry, material);
        // 		scene.add(line);
        // 	}
        // });

        // renderer.render(scene, camera);
      });

      const animate = () => {
        requestAnimationFrame(animate);
        renderer.render(scene, camera);
      };

      animate();
    },
    onMouseMove(event) {
      // mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
      // mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;
      // raycaster.setFromCamera(mouse, camera);
      // // const intersects = raycaster.intersectObjects([cuttingPlane]);
      // if (intersects.length > 0) {
      // 	const { point } = intersects[0];
      // 	cuttingPlane.position.copy(point);
      // }
    },

    // it is from public/models/skeleton.swc
    /**# SWC format file
  # based on specifications at http://www.neuronland.org/NLMorphologyConverter/MorphologyFormats/SWC/Spec.html
  # Created on 2024-03-10 using skeletor (https://github.com/navis-org/skeletor)
  # PointNo Label X Y Z Radius Parent
  # Labels:
  # 0 = undefined, 1 = soma, 5 = fork point, 6 = end point
  0 0 254.1565229829058 603.1588431791312 75.67268294608911 69.34071461914615 -1
  
  1 0 256.5360779589159 604.4241092291602 76.14282393691563 69.59244597695752 0
  
  2 6 259.3283340866501 555.8905705632391 189.80038410908466 19.44872744026625 3
  
  3 0 255.6844561392801 558.5806188750686 182.72241831104657 19.311052861978602 5
  
  4 0 260.7655211267753 606.9228221795125 78.5246554811985 66.54053540552631 1
  
  5 0 255.73786045206484 562.7503240755564 174.08133893455965 75.09439605323414 7
  
  6 0 264.9614603646989 608.7069936995644 83.05110304378515 60.897729188535386 4
  
  7 0 259.7024365579315 566.4070438402975 163.5787728877045 68.0134588270306 9
  
  8 5 269.43285765496046 610.3780299506269 85.17334314469458 59.31893804979072 6
  
  9 0 262.81074098178317 571.3735130173819 153.0086348227092 56.91943530099444 11
  
  10 6 276.0 590.2000122070312 132.0 6.0321705111251545 12
  
  11 0 265.0470720572301 577.6323872600418 142.77633489175622 49.07246939813506 12
  
  12 5 266.71338427035295 584.7686667017999 132.14541591022507 41.2121263791699 13
  
  13 0 267.45185927112374 591.1786501712211 121.12013309047435 50.24705282329434 8
  
  14 0 274.19152069091797 629.5906745062935 50.12849899855527 52.679267345096264 8
  
  15 0 275.96094462837857 634.3369428296934 38.137687113913316 46.13146600125387 14
  
  16 6 276.87497839939687 639.646396127696 25.876048114497955 51.438318768267706 15
  
   */
    // I just tell you the format of the file, and you can use the following code to load the file and draw it
    // please analyze the file and draw it
    // you just analyze it
    // write the function
    // code
    // code now
  },
};
</script>

<style scoped>
#three-container {
  width: 600px;
  height: 400px;
}

/* make gui element in parent right up */
/* .dg.ac {

    top: 11.75%;
    left: 0;
    right: 150px;
    height: 0;
    z-index: 0;
} */
</style>