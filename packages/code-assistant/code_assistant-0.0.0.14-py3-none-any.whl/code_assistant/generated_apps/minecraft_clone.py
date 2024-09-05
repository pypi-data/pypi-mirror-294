from fasthtml.common import *

app = FastHTML()
rt = app.route

@rt('/')
def get():
    return Html(
        Head(
            Title('Minecraft Clone'),
            Script(src='https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js'),
            Script(src='https://unpkg.com/htmx.org@1.6.1'),
            Script(src='https://unpkg.com/htmx.org/dist/ext/json-enc.js'),
            Style('''
                body { margin: 0; overflow: hidden; }
                canvas { display: block; }
            ''')
        ),
        Body(
            Div(id='minecraft-game'),
            Script('''
                const scene = new THREE.Scene();
                const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
                const renderer = new THREE.WebGLRenderer();
                renderer.setSize(window.innerWidth, window.innerHeight);
                document.body.appendChild(renderer.domElement);

                const geometry = new THREE.BoxGeometry();

                function createBlock(x, y, z, color) {
                    const material = new THREE.MeshBasicMaterial({ color });
                    const block = new THREE.Mesh(geometry, material);
                    block.position.set(x, y, z);
                    return block;
                }

                const blocks = [];
                for (let x = -5; x <= 5; x++) {
                    for (let z = -5; z <= 5; z++) {
                        const color = Math.random() * 0xffffff;
                        const block = createBlock(x, 0, z, color);
                        scene.add(block);
                        blocks.push(block);
                    }
                }

                camera.position.set(0, 10, 15);
                camera.lookAt(0, 0, 0);

                const raycaster = new THREE.Raycaster();
                const mouse = new THREE.Vector2();

                function onMouseClick(event) {
                    mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
                    mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;
                    raycaster.setFromCamera(mouse, camera);

                    const intersects = raycaster.intersectObjects(blocks);
                    if (intersects.length > 0) {
                        const intersect = intersects[0];
                        const newBlock = createBlock(
                            Math.round(intersect.point.x + intersect.face.normal.x),
                            Math.round(intersect.point.y + intersect.face.normal.y),
                            Math.round(intersect.point.z + intersect.face.normal.z),
                            Math.random() * 0xffffff
                        );
                        scene.add(newBlock);
                        blocks.push(newBlock);
                    }
                }

                document.addEventListener('mousedown', onMouseClick, false);

                document.addEventListener('wheel', (event) => {
                    camera.position.z += event.deltaY * 0.05;
                });

                function animate() {
                    requestAnimationFrame(animate);
                    renderer.render(scene, camera);
                }

                animate();
            ''', type='module')
        )
    )

serve()