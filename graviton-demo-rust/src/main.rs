extern crate chrono;
extern crate ec2_instance_metadata;
extern crate rustc_version_runtime;

use actix_web::{get, web, Responder, Result};
use chrono::offset::Utc;
use chrono::DateTime;
use serde::Serialize;
use std::time::SystemTime;

#[derive(Serialize, Debug)]
pub struct RuntimeInfo {
    pub instance_id: String,
    pub instance_type: String,
    pub instance_az: String,
    pub rust_version: String,
    pub timestamp: String,
}

impl std::fmt::Display for RuntimeInfo {
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
        write!(f, "{:?}", self)
    }
}

#[derive(Debug, Default)]
pub struct RuntimeInfoClient;

impl RuntimeInfoClient {
    pub fn new() -> Self {
        Self {}
    }
    pub fn get_runtime_info(&self) -> Result<RuntimeInfo, std::io::Error> {
        let client = ec2_instance_metadata::InstanceMetadataClient::new();
        let metadata = client.get().unwrap();

        let system_time = SystemTime::now();
        let datetime: DateTime<Utc> = system_time.into();

        let runtime_info = RuntimeInfo {
            instance_id: metadata.instance_id,
            instance_type: metadata.instance_type,
            instance_az: metadata.availability_zone,
            rust_version: rustc_version_runtime::version().to_string(),
            timestamp: datetime.format("%Y-%m-%d %T").to_string(),
        };
        return Ok(runtime_info);
    }
}

#[get("/")]
async fn index() -> Result<impl Responder> {
    let client = RuntimeInfoClient::new();
    let runtime_info = client.get_runtime_info().unwrap();
    Ok(web::Json(runtime_info))
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    use actix_web::{App, HttpServer};

    HttpServer::new(|| App::new().service(index))
        .bind(("0.0.0.0", 9080))?
        .run()
        .await
}
