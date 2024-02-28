<template>
    <div id="three-container"></div>
  </template>
  
  <script>
  import * as THREE from 'three';
  import { STLLoader } from 'three/examples/jsm/loaders/STLLoader';
  import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls';
  let scene = null
  let camera = null
  let renderer = null
  let planeGeometry = null
  let planeMaterial = null
  let cuttingPlane = null
  let raycaster =  null
  let mouse = null

  export default {
  
  
    mounted() {
      this.initThreeJS();
      window.addEventListener('mousemove', this.onMouseMove);
    },
    beforeDestroy() {
      window.removeEventListener('mousemove', this.onMouseMove);
    },
  
    methods: {
      initThreeJS() {
         scene = new THREE.Scene();
         camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        camera.position.z = 5;
  
         renderer = new THREE.WebGLRenderer();
        renderer.setSize(window.innerWidth, window.innerHeight);
        document.getElementById('three-container').appendChild(renderer.domElement);
  
        const ambientLight = new THREE.AmbientLight(0x404040);
        scene.add(ambientLight);
  
        const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
        directionalLight.position.set(1, 1, 1);
        scene.add(directionalLight);
  
        // STL 文件加载
        const loader = new STLLoader();
        loader.load('/models/output.stl', (geometry) => {
          geometry.computeVertexNormals(); // 计算顶点法线以平滑化
  
          const material = new THREE.MeshPhongMaterial({ color: 0x00ff00 });
          const mesh = new THREE.Mesh(geometry, material);
          scene.add(mesh);
  
          // 计算模型的边界框并居中
          const boundingBox = new THREE.Box3().setFromObject(mesh);
          const center = boundingBox.getCenter(new THREE.Vector3());
          mesh.position.x += (mesh.position.x - center.x);
          mesh.position.y += (mesh.position.y - center.y);
          mesh.position.z += (mesh.position.z - center.z);
          
          // 更新摄像机位置
          camera.lookAt(center);
        });
  
        const controls = new OrbitControls(camera, renderer.domElement);
        controls.addEventListener('change', () => renderer.render(scene, camera));
  
        const animate = () => {
          requestAnimationFrame(animate);
          renderer.render(scene, camera);
        };
  
        animate();
  
         planeGeometry = new THREE.PlaneGeometry(200, 200);
         planeMaterial = new THREE.MeshBasicMaterial({color: 0xff0000, side: THREE.DoubleSide});
        cuttingPlane = new THREE.Mesh(planeGeometry, planeMaterial);
        cuttingPlane.visible = false; // 初始状态不可见
        scene.add(cuttingPlane);
  
      },
      onMouseMove(event) {
        // 将鼠标位置转换为归一化设备坐标（NDC）
        mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
        mouse.y = - (event.clientY / window.innerHeight) * 2 + 1;
  
        // 更新射线发射器位置
        // raycaster.setFromCamera(mouse, camera);
        // const intersects = this.raycaster.intersectObjects(scene.children);
  
        // if (intersects.length > 0) {
        //   // 使切平面与交点对齐
        //   const intersect = intersects[0];
        //   cuttingPlane.position.copy(intersect.point);
        //   cuttingPlane.visible = true;
        // } else {
        //   cuttingPlane.visible = false; // 当不与模型相交时不显示
        // }
      },
    }
  };
  </script>
  
  <style>
  #three-container {
    width: 40%;
    height: 40vh;
  }
  </style>
  