using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class AttackSequence : MonoBehaviour {

    Quaternion originalRot;
    float rotX, rotY, rotZ;
    public bool isAnim;

	// Use this for initialization
	void Start () {
        originalRot = gameObject.transform.rotation;
        isAnim = true;
	}
	
	// Update is called once per frame
	void Update () {
        rotX += 5f;
        if (isAnim)
            gameObject.transform.rotation = Quaternion.Euler(new Vector3(rotX, rotY, rotZ));
        else
            gameObject.transform.rotation = originalRot;

        if (Input.GetKeyDown(KeyCode.Space))
            isAnim = !isAnim;
    }
}
