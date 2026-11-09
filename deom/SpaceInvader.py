from http.server import BaseHTTPRequestHandler, HTTPServer

HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Space Invaders</title>
    <style>
        body {
            background-color: #111;
            color: #fff;
            font-family: 'Courier New', Courier, monospace;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
            margin: 0;
            overflow: hidden;
              }
        h1 {
            margin: 5px;
            font-size: 24px;
            letter-spacing: 2px;
            color: #00ff00;
        }
        canvas {
            border: 4px solid #00ff00;
            box-shadow: 0 0 20px rgba(0, 255, 0, 0.5);
            background-color: #000;
        }
        .instructions {
            margin-top: 10px;
            font-size: 14px;
            color: #aaa;
        }
    </style>
</head>
<body>

    <h1>SPACE INVADERS</h1>
    <canvas id="gameCanvas" width="480" height="600"></canvas>
    <div class="instructions">Use <b>Left/Right Arrows</b> to move, <b>Spacebar</b> to shoot.</div>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");

        // Game State
        let score = 0;
        let lives = 3;
        let gameOver = false;
        let gameWon = false;

        // Input
        const keys = {};
        window.addEventListener("keydown", (e) => {
            if (e.code === "Space" || e.code === "ArrowLeft" || e.code === "ArrowRight") {
                e.preventDefault(); // Prevent page scrolling
            }
            keys[e.code] = true;
        });
        window.addEventListener("keyup", (e) => {
            keys[e.code] = false;
        });

        // Player
        const player = {
            x: canvas.width / 2 - 15,
            y: canvas.height - 40,
            width: 30,
            height: 16,
            speed: 5
        };

        // Bullets
        let playerBullets = [];
        let alienBullets = [];

        // Aliens
        let aliens = [];
        const alienRows = 4;
        const alienCols = 8;
        let alienDirection = 1;
        let alienSpeed = 1;
        let alienDropTimer = 0;

        function initAliens() {
            aliens = [];
            for (let r = 0; r < alienRows; r++) {
                for (let c = 0; c < alienCols; c++) {
                    aliens.push({
                        x: 50 + c * 50,
                        y: 60 + r * 35,
                        width: 24,
                        height: 16,
                        alive: true,
                        type: r === 0 ? 3 : (r < 3 ? 2 : 1) // Different point values/rows
                    });
                }
            }
        }

        // Shields / Bunkers
        let shields = [];
        function initShields() {
            shields = [];
            const shieldCount = 4;
            const spacing = canvas.width / (shieldCount + 1);
            for (let i = 0; i < shieldCount; i++) {
                shields.push({
                    x: spacing * (i + 1) - 30,
                    y: canvas.height - 110,
                    width: 60,
                    height: 25,
                    health: 10
                });
            }
        }

        function resetGame() {
            score = 0;
            lives = 3;
            gameOver = false;
            gameWon = false;
            player.x = canvas.width / 2 - 15;
            playerBullets = [];
            alienBullets = [];
            initAliens();
            initShields();
        }

        // Initialization
        initAliens();
        initShields();

        // Game Loop Update
        function update() {
            if (gameOver || gameWon) {
                if (keys["KeyR"]) {
                    resetGame();
                }
                return;
            }

            // Player Movement
            if (keys["ArrowLeft"] && player.x > 0) {
                player.x -= player.speed;
            }
            if (keys["ArrowRight"] && player.x + player.width < canvas.width) {
                player.x += player.speed;
            }

            // Player Shooting
            if (keys["Space"]) {
                if (playerBullets.length < 3) { // Limit concurrent bullets
                    // Check if enough time has passed since last shot
                    if (!player.lastShot || Date.now() - player.lastShot > 300) {
                        playerBullets.push({
                            x: player.x + player.width / 2 - 2,
                            y: player.y,
                            width: 4,
                            height: 10,
                            speed: 7
                        });
                        player.lastShot = Date.now();
                    }
                }
            }

            // Update Player Bullets
            for (let i = playerBullets.length - 1; i >= 0; i--) {
                let b = playerBullets[i];
                b.y -= b.speed;

                // Off screen check
                if (b.y < 0) {
                    playerBullets.splice(i, 1);
                    continue;
                }

                // Check collision with Shields
                let hitShield = false;
                for (let s of shields) {
                    if (s.health > 0 && b.x > s.x && b.x < s.x + s.width && b.y > s.y && b.y < s.y + s.height) {
                        s.health--;
                        hitShield = true;
                        break;
                    }
                }
                if (hitShield) {
                    playerBullets.splice(i, 1);
                    continue;
                }

                // Check collision with Aliens
                let hitAlien = false;
                for (let a of aliens) {
                    if (a.alive && b.x > a.x && b.x < a.x + a.width && b.y > a.y && b.y < a.y + a.height) {
                        a.alive = false;
                        score += a.type * 10;
                        hitAlien = true;
                        break;
                    }
                }
                if (hitAlien) {
                    playerBullets.splice(i, 1);
                }
            }

            // Check Win Condition (All aliens dead)
            if (aliens.every(a => !a.alive)) {
                gameWon = true;
                return;
            }

            // Update Aliens
            let edgeReached = false;
            for (let a of aliens) {
                if (!a.alive) continue;
                a.x += alienSpeed * alienDirection;
                if (a.x + a.width >= canvas.width - 10 || a.x <= 10) {
                    edgeReached = true;
                }
                // Check if aliens reached player level
                if (a.y + a.height >= player.y) {
                    gameOver = true;
                }
            }

            if (edgeReached) {
                alienDirection *= -1;
                for (let a of aliens) {
                    a.y += 15;
                }
            }

            // Alien Shooting Logic
            if (Math.random() < 0.02) { // Random chance to fire per frame
                let aliveAliens = aliens.filter(a => a.alive);
                if (aliveAliens.length > 0) {
                    let shooter = aliveAliens[Math.floor(Math.random() * aliveAliens.length)];
                    alienBullets.push({
                        x: shooter.x + shooter.width / 2 - 2,
                        y: shooter.y + shooter.height,
                        width: 4,
                        height: 10,
                        speed: 4
                    });
                }
            }

            // Update Alien Bullets
            for (let i = alienBullets.length - 1; i >= 0; i--) {
                let b = alienBullets[i];
                b.y += b.speed;

                // Off screen check
                if (b.y > canvas.height) {
                    alienBullets.splice(i, 1);
                    continue;
                }

                // Check collision with Shields
                let hitShield = false;
                for (let s of shields) {
                    if (s.health > 0 && b.x > s.x && b.x < s.x + s.width && b.y > s.y && b.y < s.y + s.height) {
                        s.health--;
                        hitShield = true;
                        break;
                    }
                }
                if (hitShield) {
                    alienBullets.splice(i, 1);
                    continue;
                }

                // Check collision with Player
                if (b.x > player.x && b.x < player.x + player.width && b.y > player.y && b.y < player.y + player.height) {
                    alienBullets.splice(i, 1);
                    lives--;
                    if (lives <= 0) {
                        gameOver = true;
                    } else {
                        // Reset player position on death
                        player.x = canvas.width / 2 - 15;
                    }
                }
            }
        }

        // Render Graphics
        function draw() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // Draw Score & Lives
            ctx.fillStyle = "#00ff00";
            ctx.font = "14px 'Courier New'";
            ctx.fillText(`SCORE: ${score}`, 20, 25);
            ctx.fillText(`LIVES: ${'♥ '.repeat(lives)}`, canvas.width - 120, 25);

            // Draw Player Ship (Classic Cannon look)
            ctx.fillStyle = "#00ff00";
            ctx.fillRect(player.x, player.y + 6, player.width, player.height - 6);
            ctx.fillRect(player.x + player.width / 2 - 3, player.y, 6, 6);

            // Draw Player Bullets
            ctx.fillStyle = "#ffffff";
            for (let b of playerBullets) {
                ctx.fillRect(b.x, b.y, b.width, b.height);
            }

            // Draw Alien Bullets
            ctx.fillStyle = "#ff3333";
            for (let b of alienBullets) {
                ctx.fillRect(b.x, b.y, b.width, b.height);
            }

            // Draw Aliens
            for (let a of aliens) {
                if (!a.alive) continue;
                ctx.fillStyle = a.type === 3 ? "#ff00ff" : (a.type === 2 ? "#00ffff" : "#ffff00");
                // Simple pixel art look for invaders
                ctx.fillRect(a.x, a.y, a.width, a.height);
                // Eyes cutouts for style
                ctx.fillStyle = "#000";
                ctx.fillRect(a.x + 4, a.y + 4, 3, 3);
                ctx.fillRect(a.x + a.width - 7, a.y + 4, 3, 3);
            }

            // Draw Shields / Bunkers
            for (let s of shields) {
                if (s.health > 0) {
                    ctx.fillStyle = `rgba(0, 255, 0, ${s.health / 10})`;
                    ctx.fillRect(s.x, s.y, s.width, s.height);
                }
            }

            // Game Over / Win Screens
            if (gameOver || gameWon) {
                ctx.fillStyle = "rgba(0, 0, 0, 0.8)";
                ctx.fillRect(0, 0, canvas.width, canvas.height);

                ctx.textAlign = "center";
                ctx.fillStyle = gameWon ? "#00ff00" : "#ff0000";
                ctx.font = "bold 28px 'Courier New'";
                ctx.fillText(gameWon ? "YOU WIN!" : "GAME OVER", canvas.width / 2, canvas.height / 2 - 20);

                ctx.fillStyle = "#ffffff";
                ctx.font = "14px 'Courier New'";
                ctx.fillText("Press 'R' to Restart", canvas.width / 2, canvas.height / 2 + 20);
                ctx.textAlign = "left"; // Reset alignment
            }
        }

        // Main Game Loop Execution
        function loop() {
            update();
            draw();
            requestAnimationFrame(loop);
        }

        requestAnimationFrame(loop);
    </script>
</body>
</html>
"""


class GameHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(HTML.encode("utf-8"))


if __name__ == "__main__":
    HTTPServer(("127.0.0.1", 8000), GameHandler).serve_forever()