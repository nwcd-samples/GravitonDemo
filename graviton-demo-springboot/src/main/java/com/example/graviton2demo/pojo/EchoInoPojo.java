package com.example.graviton2demo.pojo;

public class EchoInoPojo {
    private String runtime;

    public String getInstanceId() {
        return instanceId;
    }

    public void setInstanceId(String instanceId) {
        this.instanceId = instanceId;
    }

    public String getInstanceType() {
        return instanceType;
    }

    public void setInstanceType(String instanceType) {
        this.instanceType = instanceType;
    }

    public String getInstanceAZ() {
        return instanceAZ;
    }

    public void setInstanceAZ(String instanceAZ) {
        this.instanceAZ = instanceAZ;
    }

    private String instanceId;
    private String instanceType;
    private String instanceAZ;

    public String getTimestamp() {
        return timestamp;
    }

    public void setTimestamp(String timestamp) {
        this.timestamp = timestamp;
    }

    private String timestamp;

    public String getRuntime() {
        return runtime;
    }

    public void setRuntime(String runtime) {
        this.runtime = runtime;
    }
}
