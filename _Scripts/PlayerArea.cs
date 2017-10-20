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
        //gameObject.transform.rotation = Quaternion.Euler(new Vector3(0, cameraEye.transform.rotation.y, 0));
        //gameObject.transform.LookAt(cameraEye.transform);
	}

    private void OnTriggerEnter(Collider other)
    {
        if (other.tag == "Lightsaber")
        {
            if (!other.GetComponent<Lightsaber>().isPlayerController)
                other.GetComponentInParent<AttackSequence>().isAnim = false;
        }
    }

    private void OnTriggerStay(Collider other)
    {
        if (other.tag == "Lightsaber")
        {
            if (!other.GetComponent<Lightsaber>().isPlayerController)
                //other.GetComponentInParent<GameObject>().GetComponentInParent<GameObject>().GetComponentInParent<LightsaberTracker>().SetupLightsaber();
                other.GetComponentInParent<AttackSequence>().isAnim = false;
        }
    }

    private void OnTriggerExit(Collider other)
    {
        if (other.tag == "Lightsaber")
        {
            if (!other.GetComponent<Lightsaber>().isPlayerController)
                other.GetComponentInParent<AttackSequence>().isAnim = true;
        }
    }
}
