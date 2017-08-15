using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class BaxterController : MonoBehaviour {

    private SteamVR_TrackedObject trackedObj;
    private Animator anim;
    private AnimatorStateInfo currentBaseState;

	// Use this for initialization
	void Start () {
        //rb = gameObject.GetComponent<Rigidbody>();
	}

    Vector3 prevLoc = Vector3.zero;

	// Update is called once per frame
	void Update () {
        Vector3 vDir = (transform.position - prevLoc) / Time.deltaTime;
        if (vDir.x > 0.5f)
        {
            Debug.Log("Right");
        }
        else if (vDir.x < -0.5f)
        {
            Debug.Log("Left");
        }

        if (vDir.z > 0.5f)
        {
            Debug.Log("Forward");
        }
        else if (vDir.z < -0.5f)
        {
            Debug.Log("Back");
        }

        prevLoc = transform.position;
    }
}
