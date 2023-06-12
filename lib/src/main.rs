use actix_web::{App, HttpServer, Responder, web};
use reqwest::Client;

async fn index() -> impl Responder {
    "Hello, world!"
}

async fn send_tic_numerals(tic_numerals: web::Json<String>) -> impl Responder {
    let response = format!("Received TIC Numerals: {}", tic_numerals);
    response
}

#[actix_rt::main]
async fn main() -> std::io::Result<()> {
    // Start the Actix-Web server
    HttpServer::new(|| {
        App::new()
            .route("/", web::get().to(index))
            .route("/send_tic_numerals", web::post().to(send_tic_numerals))
    })
    .bind("127.0.0.1:5000")?
    .run()
    .await
}

#[tokio::test]
async fn test_index() {
    let client = Client::new();
    let response = client.get("http://127.0.0.1:5000/").send().await.unwrap();
    assert_eq!(response.status().as_u16(), 200);
    let body = response.text().await.unwrap();
    assert_eq!(body, "Hello, world!");
}

#[tokio::test]
async fn test_send_tic_numerals() {
    let client = Client::new();
    let tic_numerals = "123456789";
    let response = client
        .post("http://127.0.0.1:5000/send_tic_numerals")
        .json(&tic_numerals)
        .send()
        .await
        .unwrap();
    assert_eq!(response.status().as_u16(), 200);
    let body = response.text().await.unwrap();
    assert_eq!(body, format!("Received TIC Numerals: {}", tic_numerals));
}