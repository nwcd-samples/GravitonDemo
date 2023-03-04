package com.example.graviton2demo.services;

import com.example.graviton2demo.pojo.EchoInoPojo;
import org.springframework.stereotype.Service;
import software.amazon.awssdk.regions.internal.util.EC2MetadataUtils;

import java.text.SimpleDateFormat;
import java.util.Calendar;


@Service
public class EchoService {

    public String getRuntimeInfo(){
        String stringRT = "";
        stringRT += System.getProperty("java.vm.name") + ",";
        stringRT += System.getProperty("java.vendor") + ",";
        stringRT += System.getProperty("java.version") + ",";
        return stringRT;
    }
    public String getOSVersion()
    {
        String stringRT = System.getProperty("os.version");
        return stringRT;

    }

    public EchoInoPojo getEchoInfo(){
        EchoInoPojo echoInoPojo = new EchoInoPojo();
        echoInoPojo.setRuntime(getRuntimeInfo());
        echoInoPojo.setOSVersion(getOSVersion());
        echoInoPojo.setInstanceAZ(EC2MetadataUtils.getAvailabilityZone());
        echoInoPojo.setInstanceId(EC2MetadataUtils.getInstanceId());
        echoInoPojo.setInstanceType(EC2MetadataUtils.getInstanceType());
        echoInoPojo.setTimestamp(new SimpleDateFormat("yyyy-MM-dd HH:mm:ss").format(Calendar.getInstance().getTime()));
        return echoInoPojo;
    }
}
