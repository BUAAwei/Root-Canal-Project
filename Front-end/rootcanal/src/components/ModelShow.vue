<template>
	<div class="Container" style="display: flex;">
		<div id="three-container"></div>
		<div id="dat-gui-container"></div>
	</div>
</template>

<script>
import * as THREE from "three";
import { STLLoader } from "three/examples/jsm/loaders/STLLoader";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls";
import * as dat from "dat.gui";

export default {
	mounted() {
		this.initThreeJS();
		setTimeout(() => {
			npm
			window.addEventListener("mousemove", this.onMouseMove);
		}, 5000);
	},
	methods: {
		initThreeJS() {
			let cuttingPlane = null;
			let mouse = new THREE.Vector2();
			let raycaster = new THREE.Raycaster();
			let scene = new THREE.Scene();
			let camera = new THREE.PerspectiveCamera(
				75,
				window.innerWidth / window.innerHeight,
				0.1,
				10000
			);

			camera.position.z = 300;
			camera.position.x = 500;
			camera.position.y = 500;
			camera.rotation.z = 100;

			const renderer = new THREE.WebGLRenderer();
			renderer.setSize(1400, 800);
			document.getElementById("three-container").appendChild(renderer.domElement);

			const ambientLight = new THREE.AmbientLight(0x404040);
			scene.add(ambientLight);

			const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
			directionalLight.position.set(1, 1, 1);
			scene.add(directionalLight);

			const loader = new STLLoader();
			var centX = 0;
			var centY = 0;
			var centZ = 0;

			loader.load("/models/output3.stl", (geometry) => {
				geometry.computeVertexNormals();
				geometry.computeBoundingBox();

				const boundingBox = new THREE.Box3();
				boundingBox.setFromObject(new THREE.Mesh(geometry));
				// center = new THREE.Vector3();
				boundingBox.getCenter(centerDistance);

				console.log("Geometry centerDistance:", centerDistance);
				varX = centerDistance.x;
				varY = centerDistance.y;
				varZ = centerDistance.z;

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
					opacity: 1.2,
					transparent: true,
					metalness: 0.3,
					roughness: 1.2,
				});
				const mesh = new THREE.Mesh(geometry, material);
				scene.add(mesh);
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






			//load a .swc file and draw it



			// loader.load("/models/output3.stl", (geometry) => {
			//   geometry.computeBoundingBox();
			//   const boundingBox = geometry.boundingBox;
			//   const sliceCount = 50;
			//   const points = [];

			//   for (let i = 0; i < sliceCount; i++) {
			// 	const z =
			// 	  boundingBox.min.z +
			// 	  (i * (boundingBox.max.z - boundingBox.min.z)) / (sliceCount - 1);
			// 	const z2 =
			// 	  boundingBox.min.z +
			// 	  ((i + 1) * (boundingBox.max.z - boundingBox.min.z)) /
			// 		(sliceCount - 1);
			// 	const sliceGeometry = new THREE.BufferGeometry();

			// 	const sliceVertices = [];
			// 	const position = geometry.attributes.position;

			// 	for (let j = 0; j < position.count; j += 3) {
			// 	  const vertexZ = position.getZ(j);
			// 	  if (
			// 		!isNaN(vertexZ) &&
			// 		isFinite(vertexZ) &&
			// 		vertexZ >= z &&
			// 		vertexZ < z2
			// 	  ) {
			// 		const vertexX = position.getX(j);
			// 		const vertexY = position.getY(j);
			// 		if (
			// 		  !isNaN(vertexX) &&
			// 		  isFinite(vertexX) &&
			// 		  !isNaN(vertexY) &&
			// 		  isFinite(vertexY)
			// 		) {
			// 		  sliceVertices.push(
			// 			new THREE.Vector3(vertexX, vertexY, vertexZ)
			// 		  );
			// 		}
			// 	  }
			// 	}

			// 	if (sliceVertices.length > 0) {
			// 	  const centerDistanceOfMass = new THREE.Vector3();
			// 	  sliceVertices.forEach((vertex) => centerDistanceOfMass.add(vertex));
			// 	  centerDistanceOfMass.divideScalar(sliceVertices.length);
			// 	  points.push(centerDistanceOfMass);
			// 	}
			//   }

			//   const curve = new THREE.CubicBezierCurve3(points);
			//   const smoothPoints = curve.getPoints(100);
			//   const ggeometry = new THREE.BufferGeometry().setFromPoints(smoothPoints);
			// //   const material = new THREE.MeshBasicMaterial({
			// // 	color: 0x00ff00,
			// // 	transparent: true,
			// // 	opacity: 0.5,
			// //   });
			// // create a PBR material
			//   const material = new THREE.MeshStandardMaterial({
			// 	// color: 0x00ff00,
			// 	// transparent: true,
			// 	opacity: 0.5,
			// 	metalness: 0.9,
			// 	roughness: 0.1,
			//   });

			//   const lline = new THREE.Line(ggeometry, material);
			//   scene.add(lline);
			// });

			const planeGeometry = new THREE.PlaneGeometry(20, 20);
			const planeMaterial = new THREE.MeshPhongMaterial({ color: 0x00ff00 });
			cuttingPlane = new THREE.Mesh(planeGeometry, planeMaterial);
			cuttingPlane.visible = true;
			scene.add(cuttingPlane);

			const controls = new OrbitControls(camera, renderer.domElement);
			controls.addEventListener("change", () => renderer.render(scene, camera));

			const gui = new dat.GUI();
			// make gui element in parent dat-gui-container
			// gui.domElement.id = "dat-gui-container";
			document.getElementById("dat-gui-container").appendChild(gui.domElement);

			const cameraFolder = gui.addFolder("Camera");
			const cameraPositionController = cameraFolder.addFolder("Position");
			cameraPositionController.add(camera.position, "x", -1000, 1000).name("X");
			cameraPositionController.add(camera.position, "y", -1000, 1000).name("Y");
			cameraPositionController.add(camera.position, "z", -1000, 1000).name("Z");
			const cameraRotationController = cameraFolder.addFolder("Rotation");
			cameraRotationController.add(camera.rotation, "x", -Math.PI, Math.PI).name("X");
			cameraRotationController.add(camera.rotation, "y", -Math.PI, Math.PI).name("Y");
			cameraRotationController.add(camera.rotation, "z", -Math.PI, Math.PI).name("Z");

			const cuttingPlaneFolder = gui.addFolder("Cutting Plane");
			cuttingPlaneFolder.add(cuttingPlane.position, "x", -100, 100).name("X");
			cuttingPlaneFolder.add(cuttingPlane.position, "y", -100, 100).name("Y");
			cuttingPlaneFolder.add(cuttingPlane.position, "z", -100, 100).name("Z");
			cuttingPlaneFolder.open();


			const fileloader = new THREE.FileLoader();
			const swcPath = '/models/my_skeleton.swc'; // 替换为您的SWC文件路径
			console.log(centerDistance+"!!!!!!!!!!!?")
			fileloader.load(swcPath, swcData => {
				const lines = swcData.split('\n');

				const points = [];
				lines.forEach(line => {
					const data = line.trim().split(' ');
					if (data.length === 7) {
						const x = parseFloat(data[2]);
						const y = parseFloat(data[3]);
						const z = parseFloat(data[4]);
						console.log(x+"?")
						
						// make x y z - centerDistance
						x -= varX;
						y -= varY;	
						z -= varZ;
						console.log(x+"...")
						const radius = parseFloat(data[5]);
						const parent = parseInt(data[6]);

						const geometry = new THREE.SphereGeometry(60, 32, 32);
						const material = new THREE.MeshBasicMaterial({ color: 0xff0000 });
						const sphere = new THREE.Mesh(geometry, material);
						sphere.position.set(x, y, z);
						scene.add(sphere);
						
						points.push({
							position: new THREE.Vector3(x, y, z),
							parentIndex: parent
						});
					}
				});
				console.log(points);
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
			mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
			mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;
			raycaster.setFromCamera(mouse, camera);
			const intersects = raycaster.intersectObjects([cuttingPlane]);
			if (intersects.length > 0) {
				const { point } = intersects[0];
				cuttingPlane.position.copy(point);
			}
		},
		loadSWCFile() {
			



		}
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