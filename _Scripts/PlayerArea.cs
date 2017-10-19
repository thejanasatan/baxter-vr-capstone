using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PlayerArea : MonoBehaviour {

    public GameObject cameraEye;

	// Use this for initialization
	void Start () {
		
	}
	
	// Update is called once per frame
	void Update () {
        gameObject.transform.position = new Vector3(cameraEye.transform.position.x, 0, cameraEye.transform.position.z);
	}
}
