use axum::{routing::post, Router, response::Json};
use serde_json::json;
use std::process::Command;
use std::time::Instant;
use tokio::net::TcpListener;

fn get_python(project_root: &std::path::Path) -> std::path::PathBuf {
    let candidates = vec![
        project_root.join(".venv").join("Scripts").join("python.exe"),
        project_root.join(".venv").join("bin").join("python"),
        project_root.join(".venv").join("bin").join("python3"),
    ];

    candidates
        .into_iter()
        .find(|p| p.exists())
        .unwrap_or_else(|| std::path::PathBuf::from("python"))
}

async fn run_pipeline() -> Json<serde_json::Value> {
    let start = Instant::now();

    let project_root = std::env::current_dir()
        .unwrap()
        .parent().unwrap()
        .to_path_buf();

    let python = get_python(&project_root);
    let script = project_root.join("scripts").join("run_data_pipeline.py");

    println!("project_root: {:?}", project_root);
    println!("python:       {:?}", python);
    println!("script:       {:?}", script);

    let output = Command::new(&python)
        .arg(&script)
        .current_dir(&project_root)
        .output();

    match output {
        Ok(result) => {
            let duration = start.elapsed().as_secs_f64();
            let stdout = String::from_utf8_lossy(&result.stdout).to_string();
            let stderr = String::from_utf8_lossy(&result.stderr).to_string();

            Json(json!({
                "status": if result.status.success() { "ok" } else { "error" },
                "duration_secs": duration,
                "output": stdout,
                "errors": stderr
            }))
        }
        Err(e) => Json(json!({
            "status": "error",
            "message": e.to_string()
        }))
    }
}

#[tokio::main]
async fn main() {
    let app = Router::new()
        .route("/pipeline/run", post(run_pipeline));

    let listener = TcpListener::bind("0.0.0.0:3000").await.unwrap();
    println!("API en http://localhost:3000");
    axum::serve(listener, app).await.unwrap();
}