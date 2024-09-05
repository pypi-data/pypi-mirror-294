use actix_web::{web, App, HttpServer, Responder, HttpResponse};
use serde::{Deserialize, Serialize};
use serde_json::Value;
use std::collections::HashMap;
use std::sync::RwLock;

#[derive(Serialize, Deserialize, Clone, Debug)]
pub struct Document {
    pub data: Value,  // Используем serde_json::Value для хранения произвольных JSON-данных
}

pub struct Database {
    storage: RwLock<HashMap<String, Document>>,
}

impl Database {
    pub fn new() -> Self {
        Database {
            storage: RwLock::new(HashMap::new()),
        }
    }

    pub fn insert(&self, key: String, doc: Document) {
        let mut storage = self.storage.write().unwrap();
        storage.insert(key, doc);
    }

    pub fn get(&self, key: &str) -> Option<Document> {
        let storage = self.storage.read().unwrap();
        storage.get(key).cloned()
    }

    pub fn delete(&self, key: &str) -> Option<Document> {
        let mut storage = self.storage.write().unwrap();
        storage.remove(key)
    }

    pub fn save_to_file(&self, filename: &str) -> std::io::Result<()> {
        let storage = self.storage.read().unwrap();
        let json = serde_json::to_string(&*storage).expect("Failed to serialize data");
        std::fs::write(filename, json)?;
        Ok(())
    }

    pub fn load_from_file(&self, filename: &str) -> std::io::Result<()> {
        let contents = std::fs::read_to_string(filename)?;
        let storage: HashMap<String, Document> = serde_json::from_str(&contents).expect("Failed to deserialize data");
        let mut db_storage = self.storage.write().unwrap();
        *db_storage = storage;
        Ok(())
    }
}

// Handlers
async fn get_document(
    db: web::Data<Database>,
    path: web::Path<String>,
) -> impl Responder {
    let key = path.into_inner();
    match db.get(&key) {
        Some(doc) => HttpResponse::Ok().json(doc),
        None => HttpResponse::NotFound().finish(),
    }
}

async fn create_document(
    db: web::Data<Database>,
    path: web::Path<String>,
    doc: web::Json<Document>,
) -> impl Responder {
    let key = path.into_inner();
    db.insert(key, doc.into_inner());
    HttpResponse::Created().finish()
}

async fn delete_document(
    db: web::Data<Database>,
    path: web::Path<String>,
) -> impl Responder {
    let key = path.into_inner();
    match db.delete(&key) {
        Some(_) => HttpResponse::Ok().finish(),
        None => HttpResponse::NotFound().finish(),
    }
}

async fn save_to_file(
    db: web::Data<Database>,
    path: web::Path<String>,
) -> impl Responder {
    let filename = path.into_inner();
    match db.save_to_file(&filename) {
        Ok(_) => HttpResponse::Ok().finish(),
        Err(e) => HttpResponse::InternalServerError().body(e.to_string()),
    }
}

async fn load_from_file(
    db: web::Data<Database>,
    path: web::Path<String>,
) -> impl Responder {
    let filename = path.into_inner();
    match db.load_from_file(&filename) {
        Ok(_) => HttpResponse::Ok().finish(),
        Err(e) => HttpResponse::InternalServerError().body(e.to_string()),
    }
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    let db = web::Data::new(Database::new());

    HttpServer::new(move || {
        App::new()
            .app_data(db.clone())
            .route("/documents/{key}", web::get().to(get_document))
            .route("/documents/{key}", web::post().to(create_document))
            .route("/documents/{key}", web::delete().to(delete_document))
            .route("/save/{filename}", web::post().to(save_to_file))
            .route("/load/{filename}", web::post().to(load_from_file))
    })
    .bind("127.0.0.1:8080")?
    .run()
    .await
}
