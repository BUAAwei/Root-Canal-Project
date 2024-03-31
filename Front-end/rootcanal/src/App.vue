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
let tube;
let tube1;
let tube2;
let tube3;
let tube4;
let mesh;
let mesh1;
let mesh2;
let mesh3;
let mesh4;
let gui = new dat.GUI();
function loadAndProcessSWC(swcData, scene) {
  const lines = swcData.split("\n").filter(line => !line.startsWith('#') && line.trim() !== '');
  const points = [];
  const childrenCount = new Map();

  // 解析数据并构建结构
  lines.forEach(line => {
    const parts = line.split(' ').map(Number);
    const [id, type, x, y, z, radius, parent] = parts;
    points[id] = { id, x, y, z, radius, parent, children: [] };
    if (parent >= 0) {
      childrenCount.set(parent, (childrenCount.get(parent) || 0) + 1);
      if (points[parent]) {
        points[parent].children.push(id);
      }
    }
  });

  const vertices = [];
  const processPoint = (id, removeIfSingleChild = true) => {
    const point = points[id];
    if (!point) return;
    const numOfChildren = childrenCount.get(id) || 0;

    if (removeIfSingleChild && numOfChildren <= 2) return;

    point.children.forEach(childId => {
      const childPoint = points[childId];
      vertices.push(point.x, point.y, point.z, childPoint.x, childPoint.y, childPoint.z);
      processPoint(childId, false);
    });
  };

  // 从无父节点的点开始处理
  points.filter(point => point && point.parent === -1).forEach(point => processPoint(point.id));

  // 创建和添加线段到场景
  const geometry = new THREE.BufferGeometry();
  geometry.setAttribute('position', new THREE.Float32BufferAttribute(vertices, 3));
  const material = new THREE.LineBasicMaterial({ color: 0xff0000 });
  const lineSegments = new THREE.LineSegments(geometry, material);
  scene.add(lineSegments);
}

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

      const directionalLight = new THREE.DirectionalLight(0xffffff, 100);
      directionalLight.position.set(1, 1, 1);
      scene.add(directionalLight);

      const loader = new STLLoader();
      const textloader = new THREE.TextureLoader();
      scene.background = new THREE.Color(0x8fbcd4); // 例如：0x8FBCD4 为天空蓝
      // Vertex Shader
      const vertexShader = `
  varying vec2 vUv;
  void main() {
    vUv = uv;
    gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
  }
`;

      // Fragment Shader
      const fragmentShader = `
      uniform sampler2D map;
varying vec2 vUv;

void main() {
  vec4 texColor = texture2D(map, vUv);
  float grayscale = (texColor.r + texColor.g + texColor.b) / 3.0;

  // 计算uv坐标与中心的距离
  // float distance = distance(vUv, vec2(0.5, 0.5));

  // 设定中间显示区域的半径大小
  // float radius = 0.5; // 可以调整这个值以改变中心显示区域的大小
  // bool cent = false;

  // 如果是中间部分，保持不变；否则，使其透明
  if(!(vUv.x > 0.2 && vUv.x < 0.8 && vUv.y > 0.05 && vUv.y < 0.95)){
    return;
  }
  if (grayscale < 0.1) {
    gl_FragColor = vec4(texColor.rgb, 0.05); // 黑色或接近黑色的像素变得半透明
  } else {
    gl_FragColor = vec4(texColor.rgb, 1); // 其他像素根据距离调整透明度
  }
}

`;
      for (let i = 1; i < 200; i += 10) {
        var texturePath = "/img/" + i + ".png";
        console.log(texturePath);
        textloader.load(texturePath, function (texture) {
          const geometry = new THREE.PlaneGeometry(200, 200);

          const material = new THREE.MeshBasicMaterial({
            map: texture,
            side: THREE.DoubleSide,
          });
          const plane = new THREE.Mesh(geometry, material);

          // 根据需要调整位置，避免图片重叠
          plane.position.set(-700, i * 2, 0);

          // 使平面竖直摆放，围绕X轴旋转90度
          plane.rotation.x = Math.PI / 2;

          scene.add(plane);
        });
      }

      for (let i = 1; i < 200; i += 3) {
        texturePath = "/mask/" + i + ".png";
        console.log(texturePath);
        textloader.load(texturePath, function (texture) {
          const geometry = new THREE.PlaneGeometry(600, 600);

          const material = new THREE.ShaderMaterial({
            uniforms: {
              map: { value: texture },
            },
            vertexShader: vertexShader,
            fragmentShader: fragmentShader,
            transparent: true, // 开启材质的透明度支持
            side: THREE.DoubleSide, // 设置材质的双面渲染
          });
          const plane = new THREE.Mesh(geometry, material);

          // 根据需要调整位置，避免图片重叠
          plane.position.set(-300, i * 2, 0);

          // 使平面竖直摆放，围绕X轴旋转90度
          plane.rotation.x = Math.PI / 2;

          scene.add(plane);
        });
      }

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
        // geometry.center();

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
        mesh1 = new THREE.Mesh(geometry, material);
        scene.add(mesh1);

        const fileloader = new THREE.FileLoader();
        const swcPath = "/models/my_skeleton.swc"; // 替换为您的SWC文件路径
        console.log(centerDistance + "!!!!!!!!!!!?");
        fileloader.load(swcPath, function(swcData) {
          const lines = swcData.split("\n").filter(line => !line.startsWith('#') && line.trim() !== '');
          const points = []; // 用于存储顶点
          const geometry = new THREE.BufferGeometry();
          const material = new THREE.LineBasicMaterial({ color: 0xff0000 });
          const vertices = [];

          lines.forEach(line => {
            const parts = line.split(' ').map(Number);
            const [id, type, x, y, z, radius, parent] = parts;

            // 将顶点坐标存储为Vector3，便于之后查找和连接
            points[id] = { x, y, z, parent };
          });

          // 创建顶点连接
          points.forEach((point, id) => {
            if (point.parent > 0) { // 忽略没有父节点的顶点（如根节点）
              const parentPoint = points[point.parent];
              if (parentPoint) {
                vertices.push(point.x, point.y, point.z);
                vertices.push(parentPoint.x, parentPoint.y, parentPoint.z);
              }
            }
          });

          // 将顶点数据传递给BufferGeometry
          geometry.setAttribute('position', new THREE.Float32BufferAttribute(vertices, 3));
          
          // 创建线段并添加到场景
          tube1 = new THREE.LineSegments(geometry, material);
          scene.add(tube1);
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






        // 一定要记得打开每个folder
        cameraFolder.open();
        // meshFolder.open();


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


      //同样的load output2 output3  output4
      loader.load("/models/output2.stl", (geometry) => {
        geometry.computeVertexNormals();
        geometry.computeBoundingBox();
        // geometry.center();
        const material = new THREE.MeshStandardMaterial({
          opacity: 0.6,
          transparent: true,
          metalness: 0.3,
          roughness: 1.2,
        });
        mesh2 = new THREE.Mesh(geometry, material);
        scene.add(mesh2);
        const fileloader = new THREE.FileLoader();
        const swcPath = "/models/output2.swc"; // 替换为您的SWC文件路径
        console.log(centerDistance + "!!!!!!!!!!!?");
        fileloader.load(swcPath, function(swcData) {
          const lines = swcData.split("\n").filter(line => !line.startsWith('#') && line.trim() !== '');
          const points = []; // 用于存储顶点
          const geometry = new THREE.BufferGeometry();
          const material = new THREE.LineBasicMaterial({ color: 0xff0000 });
          const vertices = [];

          lines.forEach(line => {
            const parts = line.split(' ').map(Number);
            const [id, type, x, y, z, radius, parent] = parts;

            // 将顶点坐标存储为Vector3，便于之后查找和连接
            points[id] = { x, y, z, parent };
          });

          // 创建顶点连接
          points.forEach((point, id) => {
            if (point.parent > 0) { // 忽略没有父节点的顶点（如根节点）
              const parentPoint = points[point.parent];
              if (parentPoint) {
                vertices.push(point.x, point.y, point.z);
                vertices.push(parentPoint.x, parentPoint.y, parentPoint.z);
              }
            }
          });

          // 将顶点数据传递给BufferGeometry
          geometry.setAttribute('position', new THREE.Float32BufferAttribute(vertices, 3));
          
          // 创建线段并添加到场景
          tube2 = new THREE.LineSegments(geometry, material);
          scene.add(tube2);
        });
        //set x
        // mesh.position.z = 100;
      });
      
      loader.load("/models/output3.stl", (geometry) => {
        geometry.computeVertexNormals();
        geometry.computeBoundingBox();
        // geometry.center();
        const material = new THREE.MeshStandardMaterial({
          opacity: 0.6,
          transparent: true,
          metalness: 0.3,
          roughness: 1.2,
        });
        mesh3 = new THREE.Mesh(geometry, material);
        scene.add(mesh3);
        const fileloader = new THREE.FileLoader();
        const swcPath = "/models/output3.swc"; // 替换为您的SWC文件路径
        fileloader.load(swcPath, function(swcData) {
          const lines = swcData.split("\n").filter(line => !line.startsWith('#') && line.trim() !== '');
          const points = []; // 用于存储顶点
          const geometry = new THREE.BufferGeometry();
          const material = new THREE.LineBasicMaterial({ color: 0xff0000 });
          const vertices = [];

          lines.forEach(line => {
            const parts = line.split(' ').map(Number);
            const [id, type, x, y, z, radius, parent] = parts;

            // 将顶点坐标存储为Vector3，便于之后查找和连接
            points[id] = { x, y, z, parent };
          });

          // 创建顶点连接
          points.forEach((point, id) => {
            if (point.parent > 0) { // 忽略没有父节点的顶点（如根节点）
              const parentPoint = points[point.parent];
              if (parentPoint) {
                vertices.push(point.x, point.y, point.z);
                vertices.push(parentPoint.x, parentPoint.y, parentPoint.z);
              }
            }
          });

          // 将顶点数据传递给BufferGeometry
          geometry.setAttribute('position', new THREE.Float32BufferAttribute(vertices, 3));
          
          // 创建线段并添加到场景
          tube3 = new THREE.LineSegments(geometry, material);
          scene.add(tube3);
        });
        // mesh.position.z = 200;
      });

      loader.load("/models/output4.stl", (geometry) => {
        geometry.computeVertexNormals();
        geometry.computeBoundingBox();
        // geometry.center();
        const material = new THREE.MeshStandardMaterial({
          opacity: 0.6,
          transparent: true,
          metalness: 0.3,
          roughness: 1.2,
        });
        mesh4 = new THREE.Mesh(geometry, material);
        scene.add(mesh4);
        const fileloader = new THREE.FileLoader();
        const swcPath = "/models/output4.swc"; // 替换为您的SWC文件路径
        console.log(centerDistance + "!!!!!!!!!!!?");
        // 假设你已经有了THREE.FileLoader的实例fileLoader和一个场景scene

        fileloader.load(swcPath, function(swcData) {
          const lines = swcData.split("\n").filter(line => !line.startsWith('#') && line.trim() !== '');
          const points = []; // 用于存储顶点
          const geometry = new THREE.BufferGeometry();
          const material = new THREE.LineBasicMaterial({ color: 0xff0000 });
          const vertices = [];

          lines.forEach(line => {
            const parts = line.split(' ').map(Number);
            const [id, type, x, y, z, radius, parent] = parts;

            // 将顶点坐标存储为Vector3，便于之后查找和连接
            points[id] = { x, y, z, parent };
          });

          // 创建顶点连接
          points.forEach((point, id) => {
            if (point.parent > 0) { // 忽略没有父节点的顶点（如根节点）
              const parentPoint = points[point.parent];
              if (parentPoint) {
                vertices.push(point.x, point.y, point.z);
                vertices.push(parentPoint.x, parentPoint.y, parentPoint.z);
              }
            }
          });

          // 将顶点数据传递给BufferGeometry
          geometry.setAttribute('position', new THREE.Float32BufferAttribute(vertices, 3));
          
          // 创建线段并添加到场景
          tube4 = new THREE.LineSegments(geometry, material);
          scene.add(tube4);
        });


                  // 假设你已经有了mesh和tube对象，以及一个dat.GUI实例gui

          const objectControls = {
            positionX: 0,
            positionY: 0,
            positionZ: 0,
            rotationX: 0,
            rotationY: 0,
            rotationZ: 0
          };

          // 更新位置
          function updatePosition() {
            mesh1.position.set(objectControls.positionX, objectControls.positionY, objectControls.positionZ);
            tube1.position.set(objectControls.positionX, objectControls.positionY, objectControls.positionZ);

            mesh2.position.set(objectControls.positionX, objectControls.positionY, objectControls.positionZ);
            tube2.position.set(objectControls.positionX, objectControls.positionY, objectControls.positionZ);

            mesh3.position.set(objectControls.positionX, objectControls.positionY, objectControls.positionZ);
            tube3.position.set(objectControls.positionX, objectControls.positionY, objectControls.positionZ);

            mesh4.position.set(objectControls.positionX, objectControls.positionY, objectControls.positionZ);
            tube4.position.set(objectControls.positionX, objectControls.positionY, objectControls.positionZ);
          }

          // 更新旋转
          // 更新旋转，将角度转换为弧度
function updateRotation() {
  const radX = objectControls.rotationX * Math.PI / 180;
  const radY = objectControls.rotationY * Math.PI / 180;
  const radZ = objectControls.rotationZ * Math.PI / 180;

  mesh1.rotation.set(radX, radY, radZ);
  tube1.rotation.set(radX, radY, radZ);

  mesh2.rotation.set(radX, radY, radZ);
  tube2.rotation.set(radX, radY, radZ);

  mesh3.rotation.set(radX, radY, radZ);
  tube3.rotation.set(radX, radY, radZ);

  mesh4.rotation.set(radX, radY, radZ);
  tube4.rotation.set(radX, radY, radZ);
}

          const guiFolder = gui.addFolder('Mesh & Tube Controls');

          // 位置控制
          guiFolder.add(objectControls, 'positionX', -1000, 1000).onChange(updatePosition);
          guiFolder.add(objectControls, 'positionY', -1000, 1000).onChange(updatePosition);
          guiFolder.add(objectControls, 'positionZ', -1000, 1000).onChange(updatePosition);

          // 旋转控制
          guiFolder.add(objectControls, 'rotationX', -360, 360).onChange(updateRotation);
          guiFolder.add(objectControls, 'rotationY', -360, 360).onChange(updateRotation);
          guiFolder.add(objectControls, 'rotationZ', -360, 360).onChange(updateRotation);

          // 假设你已经有了mesh和tube对象，以及一个dat.GUI实例gui

          // 扩展objectControls对象以包括scale属性
          objectControls.scaleX = 1;
          objectControls.scaleY = 1;
          objectControls.scaleZ = 1;

          // 更新缩放的函数
          function updateScale() {
            mesh1.scale.set(objectControls.scaleX, objectControls.scaleY, objectControls.scaleZ);
            tube1.scale.set(objectControls.scaleX, objectControls.scaleY, objectControls.scaleZ);

            mesh2.scale.set(objectControls.scaleX, objectControls.scaleY, objectControls.scaleZ);
            tube2.scale.set(objectControls.scaleX, objectControls.scaleY, objectControls.scaleZ);

            mesh3.scale.set(objectControls.scaleX, objectControls.scaleY, objectControls.scaleZ);
            tube3.scale.set(objectControls.scaleX, objectControls.scaleY, objectControls.scaleZ);

            mesh4.scale.set(objectControls.scaleX, objectControls.scaleY, objectControls.scaleZ);
            tube4.scale.set(objectControls.scaleX, objectControls.scaleY, objectControls.scaleZ);
          }

          // 添加到GUI
          guiFolder.add(objectControls, 'scaleX', 0, 5).name('Scale X').onChange(updateScale);
          guiFolder.add(objectControls, 'scaleY', 0, 5).name('Scale Y').onChange(updateScale);
          guiFolder.add(objectControls, 'scaleZ', 0, 5).name('Scale Z').onChange(updateScale);

          guiFolder.open();


        // mesh.position.z = 300;
      });
      const animate = () => {
        requestAnimationFrame(animate);
        renderer.render(scene, camera);
        // console.log(tube);
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