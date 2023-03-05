extern crate chrono;
extern crate ec2_instance_metadata;
extern crate rustc_version_runtime;

use std::{
    io::{prelude::*, BufReader},
    net::{TcpListener, TcpStream},
    thread,
};


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

fn main() {
    let listener = TcpListener::bind("0.0.0.0:5006").unwrap();

    for stream in listener.incoming() {
        let stream = stream.unwrap();

        thread::spawn(|| {
            handle_connection(stream);
        });
    }
}
fn handle_connection(mut stream: TcpStream) {

    let buf_reader = BufReader::new(&mut stream);
    let request_line = buf_reader.lines().next().unwrap().unwrap();
    
    let client = RuntimeInfoClient::new();
    let runtime_info = client.get_runtime_info().unwrap();

    //if request_line == "GET / HTTP/1.1" {
    if request_line != "" {
        let status_line = "HTTP/1.1 200 OK";
        let contents_begin = "<html><body><h1>Graviton University Rust Demo</h1>";
        let contents_end="</body></html>";
        let contents = format!("{}<p>Instance Type : {}</p><p>Instance ID : {}</p><p>Instance AZ : {}</p><p>Runtime Version is : {}</p><p>TimeStamp is : {}</p>{}",  contents_begin,runtime_info.instance_type,runtime_info.instance_id,runtime_info.instance_az,runtime_info.rust_version,runtime_info.timestamp,contents_end);
        let length = contents.len();

        let response = format!(
            "{status_line}\r\nContent-Length: {length}\r\n\r\n{contents}"
        );

        stream.write_all(response.as_bytes()).unwrap();
    } else {
        // some other request
    }
}
